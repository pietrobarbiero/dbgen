import traceback

import pandas as pd
from mongoengine import Document, StringField, errors, ReferenceField

from . import sample

PHENOTYPE = (('R', 'Resistant'),
            ('S', 'Susceptible'),
            ('I', 'Intermediate'))


class Phenotype(Document):
    name = StringField(max_length=200, required=True, unique_with='sample')
    phenotype = StringField(max_length=3, required=True, choices=PHENOTYPE)
    sample = ReferenceField('Sample', required=True, unique_with='name')


def import_data(dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        for _, row in df.iterrows():
            run_accession = row[2]
            for pname, phenotype in row.items():
                if pname not in ["ENA project", "Fastq reads", "Run accession"]:
                    try:
                        s = sample.Sample.objects(pk=run_accession).first()
                        Phenotype.objects(sample=run_accession, name=pname).\
                            update_one(set__name=pname, set__phenotype=phenotype,
                                       set__sample=s, upsert=True)
                        p = Phenotype.objects(sample=run_accession, name=pname).first()
                        sample.Sample.objects(pk=run_accession).update(add_to_set__phenotypes__=p.pk)
                    except errors.ValidationError:
                        continue
                        # print(traceback.format_exc())
