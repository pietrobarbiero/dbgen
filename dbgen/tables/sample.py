import os
import traceback

import pandas as pd
from mongoengine import Document, StringField, ListField, errors, ReferenceField, queryset_manager

from . import dataset, species
from .result import Result


class Sample(Document):
    run_accession = StringField(max_length=200, unique=True)
    download_urls = ListField(StringField(max_length=200))
    raw_data = StringField(max_length=200)
    cooked_data = ListField(ReferenceField('Result'))
    phenotypes = ListField(ReferenceField('Phenotype'))
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_download_urls(doc_cls, queryset, species_name=None, dataset_name=None):
        if species_name and dataset_name:
            s = species.Species.objects(name=species_name).first()
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(species=s, dataset=d)
        elif (not species_name) and dataset_name:
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(dataset=d)
        elif species_name and (not dataset_name):
            s = species.Species.objects(name=species_name).first()
            data = queryset.filter(species=s)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_url(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_raw_data(doc_cls, queryset, species_name=None, dataset_name=None):
        if species_name and dataset_name:
            s = species.Species.objects(name=species_name).first()
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(species=s, dataset=d)
        elif (not species_name) and dataset_name:
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(dataset=d)
        elif species_name and (not dataset_name):
            s = species.Species.objects(name=species_name).first()
            data = queryset.filter(species=s)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_raw(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_results(doc_cls, queryset, species_name=None, dataset_name=None):
        if species_name and dataset_name:
            s = species.Species.objects(name=species_name).first()
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(species=s, dataset=d)
        elif (not species_name) and dataset_name:
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(dataset=d)
        elif species_name and (not dataset_name):
            s = species.Species.objects(name=species_name).first()
            data = queryset.filter(species=s)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_results(d)
            df = df.append(ds)
        return df

    @staticmethod
    def save_result(sample_id, tool, version, date, parameters, raw_result_path):
        s = Sample.objects(pk=sample_id).first()
        Result.objects(tool=tool, version=version, parameters=parameters). \
            update_one(set__tool=tool, set__version=version,
                       set__date=date, set__parameters=parameters, upsert=True)
        r = Result.objects(tool=tool, version=version, parameters=parameters).first()
        with open(raw_result_path, 'rb') as fd:
            r.raw_result.replace(fd, content_type='text')
        r.save()
        s.update(add_to_set__cooked_data__=r)
        # s = Sample.objects(run_accession=sample_id).first()
        # q = s.cooked_data[0].raw_result.read()


def _to_df_results(s: Sample):
    df_results = pd.DataFrame()
    for result in s.cooked_data:
        d = {s.pk: (s.run_accession, s.species.name, s.dataset.name,
                    result.tool, result.version, result.date, result.parameters, result.raw_result)}
        df = pd.DataFrame.from_dict(d, orient="index", columns=["run_accession", "species", "dataset",
                                                                "tool", "version", "date", "parameters", "raw_result"])
        df_results = df_results.append(df)
    return df_results


def _to_df_raw(s: Sample):
    d = {s.pk: (s.run_accession, s.species.name, s.dataset.name, s.raw_data)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["run_accession", "species", "dataset", "fastq_dir"])
    return df


def _to_df_url(s: Sample):
    d = {s.pk: (s.run_accession, s.species.name, s.dataset.name, s.download_urls)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["run_accession", "species", "dataset", "url"])
    return df


def import_data(configs, dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        for _, row in df.iterrows():
            run_accession = row[2]
            download_urls = row[1].split(";")
            base_id = run_accession[:6]
            source = row[0]
            raw_data = os.path.join(configs.fastq_dir, source, base_id, run_accession)
            try:
                sp = species.Species.objects(name=configs.species).first()
                dt = dataset.Dataset.objects(name=dname).first()
                Sample.objects(run_accession=run_accession). \
                    update_one(set__run_accession=run_accession, set__download_urls=download_urls,
                               set__species=sp, set__dataset=dt, set__raw_data=raw_data,
                               upsert=True)
                s = Sample.objects(run_accession=run_accession).first()
                dataset.Dataset.objects(name=dname).update(add_to_set__samples__=s)
            except errors.ValidationError:
                continue
                # print(traceback.format_exc())
