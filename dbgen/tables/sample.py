import traceback

import pandas as pd
from mongoengine import Document, StringField, ListField, errors, ReferenceField, queryset_manager

from . import dataset, species


class Sample(Document):
    run_accession = StringField(max_length=200, primary_key=True)
    download_urls = ListField(StringField(max_length=200))
    fastq_directory = StringField(max_length=200)
    phenotypes = ListField(ReferenceField('Phenotype'))
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_download_urls(doc_cls, queryset, species_name=None, dataset_name=None):
        if species_name and dataset_name:
            data = queryset.filter(species=species_name, dataset=dataset_name)
        elif (not species_name) and dataset_name:
            data = queryset.filter(dataset=dataset_name)
        elif species_name and (not dataset_name):
            data = queryset.filter(species=species_name)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_url(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_fastq_dirs(doc_cls, queryset, species_name=None, dataset_name=None):
        if species_name and dataset_name:
            data = queryset.filter(species=species_name, dataset=dataset_name)
        elif (not species_name) and dataset_name:
            data = queryset.filter(dataset=dataset_name)
        elif species_name and (not dataset_name):
            data = queryset.filter(species=species_name)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df_fastq(d)
            df = df.append(ds)
        return df


def _to_df_fastq(s: Sample):
    d = {s.pk: (s.species.name, s.dataset.name, s.fastq_directory)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["species", "dataset", "fastq_dir"])
    return df


def _to_df_url(s: Sample):
    d = {s.pk: (s.species.name, s.dataset.name, s.download_urls)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["species", "dataset", "url"])
    return df


def import_data(species_name, dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        for _, row in df.iterrows():
            run_accession = row[2]
            download_urls = row[1].split(";")
            try:
                sp = species.Species.objects(pk=species_name).first()
                dt = dataset.Dataset.objects(pk=dname).first()
                Sample.objects(run_accession=run_accession). \
                    update_one(set__run_accession=run_accession, set__download_urls=download_urls,
                               set__species=sp, set__dataset=dt, upsert=True)
                dataset.Dataset.objects(pk=dname).update(add_to_set__samples__=run_accession)
            except errors.ValidationError:
                continue
                # print(traceback.format_exc())
