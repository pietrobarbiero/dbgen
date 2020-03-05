import traceback

import pandas as pd
from mongoengine import Document, StringField, ListField, errors, ReferenceField

from . import dataset


class Sample(Document):
    run_accession = StringField(max_length=200, primary_key=True)
    download_urls = ListField(StringField(max_length=200))
    fastq_directory = StringField(max_length=200)
    phenotypes = ListField(ReferenceField('Phenotype'))


def import_data(dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        for _, row in df.iterrows():
            run_accession = row[2]
            download_urls = row[1].split(";")
            try:
                Sample.objects(run_accession=run_accession). \
                    update_one(set__run_accession=run_accession, set__download_urls=download_urls, upsert=True)
                dataset.Dataset.objects(pk=dname).update(add_to_set__samples__=run_accession)
            except errors.ValidationError:
                continue
                # print(traceback.format_exc())
