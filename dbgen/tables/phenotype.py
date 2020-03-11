import traceback

import pandas as pd
from mongoengine import Document, StringField, errors, ReferenceField, queryset_manager

from . import sample, dataset, species

PHENOTYPE = (('R', 'Resistant'),
            ('S', 'Susceptible'),
            ('I', 'Intermediate'))


class Phenotype(Document):
    name = StringField(max_length=200, required=True, unique_with='sample')
    phenotype = StringField(max_length=3, required=True, choices=PHENOTYPE)
    sample = ReferenceField('Sample', required=True, unique_with='name')
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_phenotypes(doc_cls, queryset, species_name=None, phenotype_name=None, dataset_name=None):
        if species_name and phenotype_name and dataset_name:
            s = species.Species.objects(name=species_name).first()
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(species=s, dataset=d, name=phenotype_name)
        elif (not species_name) and phenotype_name and dataset_name:
            d = dataset.Dataset.objects(name=dataset_name).first()
            data = queryset.filter(dataset=d, name=phenotype_name)
        elif species_name and phenotype_name and (not dataset_name):
            s = species.Species.objects(name=species_name).first()
            data = queryset.filter(species=s, name=phenotype_name)
        else:
            return pd.DataFrame()
        df = pd.DataFrame()
        for d in data:
            ds = _to_df(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_phenotype_names(doc_cls, queryset, species_name=None):
        if species_name:
            s = species.Species.objects(name=species_name).first()
            data = queryset.filter(species=s)
        else:
            return pd.DataFrame()
        names = set()
        for d in data:
            names.add(d.name)
        return names


def _to_df(ph: Phenotype):
    d = {ph.sample.pk: (ph.species.name, ph.dataset.name, ph.phenotype)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["species", "dataset", ph.name])
    return df


def import_data(configs, dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        for _, row in df.iterrows():
            run_accession = row[2]
            for pname, phenotype in row.items():
                if pname not in ["ENA project", "Fastq reads", "Run accession"]:
                    try:
                        s = sample.Sample.objects(run_accession=run_accession).first()
                        sp = species.Species.objects(name=configs.species).first()
                        dt = dataset.Dataset.objects(name=dname).first()
                        Phenotype.objects(sample=s, name=pname).\
                            update_one(set__name=pname, set__phenotype=phenotype,
                                       set__sample=s, set__species=sp,
                                       set__dataset=dt, upsert=True)
                        p = Phenotype.objects(sample=s, name=pname).first()
                        sample.Sample.objects(run_accession=run_accession).update(add_to_set__phenotypes__=p)
                    except errors.ValidationError:
                        continue
                        # print(traceback.format_exc())
