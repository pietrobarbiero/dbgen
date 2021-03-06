import json
import os
import traceback
import urllib.request
from argparse import Namespace
from typing import List

from ftplib import FTP
import pandas as pd
from mongoengine import Document, StringField, ListField, errors, ReferenceField, queryset_manager, QuerySet, FileField, \
    GridFSProxy, EmbeddedDocument, EmbeddedDocumentListField

from . import dataset, species
from .result import Result
from ..utils.config import _options


class RawFile(EmbeddedDocument):
    url = StringField(max_length=200, primary_key=True)
    name = StringField(max_length=200)
    file = FileField()


class Sample(Document):
    """
    Sample

    Attributes
    ----------
    :param project: project code (e.g. ENA project)
    :param run_accession: accession number
    :param download_urls: list of URLs to download genome data
    :param raw_data: file path to raw files (downloaded genome data)
    :param cooked_data: list of references to results generated by bioinformatics tools
    :param phenotypes: list of references to phenotypes
    :param dataset: reference to sample dataset
    :param species: reference to sample species
    """
    project = StringField(max_length=200, unique_with=["run_accession"])
    run_accession = StringField(max_length=200, unique_with=["project"])
    download_urls = ListField(StringField(max_length=200))
    raw_data = EmbeddedDocumentListField(RawFile)
    cooked_data = ListField(ReferenceField('Result'))
    phenotypes = ListField(ReferenceField('Phenotype'))
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_download_urls(doc_cls, queryset: QuerySet,
                          species_name: str = None, dataset_name: str = None) -> pd.DataFrame:
        """
        Get the URLs to download sample genomes

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        """
        data = _options(queryset, species_name, dataset_name)
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_url(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_raw_data(doc_cls, queryset: QuerySet,
                     species_name: str = None, dataset_name: str = None) -> pd.DataFrame:
        """
        Get local paths to raw genomes

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        """
        data = _options(queryset, species_name, dataset_name)
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_raw(d)
            df = df.append(ds)
        return df

    @staticmethod
    def save_result(sample_id: str, tool: str, version: str,
                    date: str, parameters: str, raw_result_path: str):
        """
        Save the output results of a bioinformatic tool

        :param sample_id: sample ID
        :param tool: bioinformatic tool name
        :param version: bioinformatic tool version
        :param date: date when the results have been collected
        :param parameters: bioinformatic tool parameters
        :param raw_result_path: path to the local output file
        """
        s = Sample.objects(pk=sample_id).first()
        Result.objects(tool=tool, version=version, parameters=parameters, sample=s.pk). \
            update_one(set__tool=tool, set__version=version,
                       set__date=date, set__parameters=parameters,
                       set__sample=s.pk, set__dataset=s.dataset, set__species=s.species,
                       upsert=True)
        r = Result.objects(tool=tool, version=version, parameters=parameters, sample=s.pk).first()
        with open(raw_result_path, 'rb') as fd:
            r.raw_result.replace(fd, content_type='text')
        r.save()
        s.update(add_to_set__cooked_data__=r)

    @staticmethod
    def download_raw_data(species_name: str = None, dataset_name: str = None):
        """
        Download raw data

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        """
        data = Sample.get_download_urls(species_name, dataset_name)
        root_path = "./.tmp/dbgen/raw/"
        if not os.path.exists(root_path):
            os.makedirs(root_path)

        data = data.iloc[:2]
        for k, v in data.iterrows():
            for url in v["url"]:
                local_file = os.path.join(root_path, url)
                local_dir = os.path.join(*local_file.split("/")[:-1])
                if not os.path.isdir(local_dir):
                    os.makedirs(local_dir)

                remote_file = os.path.join("ftp://", url)
                if not os.path.isfile(local_file):
                    urllib.request.urlretrieve(remote_file, local_file)

                s = Sample.objects(pk=k).first()
                is_present = False
                for f in s.raw_data:
                    if f.url == url:
                        is_present = True
                        break

                if not is_present:
                    r = RawFile()
                    r.url = url
                    r.name = url.split("/")[-1]
                    with open(local_file, 'rb') as fd:
                        r.file.put(fd)
                    s.update(add_to_set__raw_data__=r, upsert=True)


def _to_df_raw(s: Sample):
    d = {s.pk: (s.project, s.run_accession, s.species.name, s.dataset.name, s.raw_data)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["project", "run accession", "species", "dataset", "raw data"])
    return df


def _to_df_url(s: Sample):
    d = {s.pk: (s.project, s.run_accession, s.species.name, s.dataset.name, s.download_urls)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["project", "run accession", "species", "dataset", "url"])
    return df


def import_data(species_name: str, dataset_name: str, dataset_file: str):
    """
    Import dataset

    Parameters
    ----------
    :param species_name: species name
    :param dataset_name: dataset names (e.g. name of the corresponding publication)
    :param dataset_file: input file path
    """
    df = pd.read_csv(dataset_file, sep="\t")
    df.dropna(axis=0, inplace=True, how="all")
    for _, row in df.iterrows():
        project = row[0]
        run_accession = row[2]
        download_urls = row[1].split(";")
        try:
            sp = species.Species.objects(name=species_name).first()
            dt = dataset.Dataset.objects(name=dataset_name).first()
            Sample.objects(project=project, run_accession=run_accession). \
                update_one(set__project=project, set__run_accession=run_accession,
                           set__download_urls=download_urls,
                           set__species=sp, set__dataset=dt, upsert=True)
            s = Sample.objects(project=project, run_accession=run_accession).first()
            dataset.Dataset.objects(name=dataset_name).update(add_to_set__samples__=s)
        except errors.ValidationError:
            continue
            # print(traceback.format_exc())
