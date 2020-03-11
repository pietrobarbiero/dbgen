import traceback
from argparse import Namespace
from typing import List, Set

import pandas as pd
from mongoengine import Document, StringField, errors, ReferenceField, queryset_manager, QuerySet

from . import sample, dataset, species
from ..utils.config import _options

PHENOTYPE = (('R', 'Resistant'),
             ('S', 'Susceptible'),
             ('I', 'Intermediate'))


class Phenotype(Document):
    """
    Phenotype

    Attributes
    ----------
    :param name: name (e.g. substance name or phenotype name)
    :param phenotype: corresponding phenotype (e.g. resistant/susceptible to a substance)
    :param sample: reference the corresponding sample
    :param dataset: reference the corresponding dataset
    :param species: reference the corresponding species
    """
    name = StringField(max_length=200, required=True, unique_with='sample')
    phenotype = StringField(max_length=3, required=True, choices=PHENOTYPE)
    sample = ReferenceField('Sample', required=True, unique_with='name')
    dataset = ReferenceField('Dataset', required=True)
    species = ReferenceField('Species', required=True)

    @queryset_manager
    def get_phenotypes(doc_cls, queryset: QuerySet,
                       species_name=None, dataset_name=None, phenotype_name=None) -> pd.DataFrame:
        """
        Get samples' phenotypes

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        :param phenotype_name: name of the phenotype
    """
        data = _options(queryset, species_name, dataset_name, phenotype_name)
        df = pd.DataFrame()
        for d in data:
            ds = _to_df(d)
            df = df.append(ds)
        return df

    @queryset_manager
    def get_phenotype_names(doc_cls, queryset: QuerySet, species_name=None) -> Set:
        """
        Get all phenotype names available for a specific species

        :param species_name: name of the species
    """
        data = _options(queryset, species_name)
        names = set()
        for d in data:
            names.add(d.name)
        return names


def _to_df(ph: Phenotype):
    d = {ph.sample.pk: (ph.species.name, ph.dataset.name, ph.phenotype)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["species", "dataset", ph.name])
    return df


def import_data(configs: Namespace, dataset_names: List, dataset_years: List, dataset_files: List):
    """
    Import new phenotypes

    Parameters
    ----------
    :param configs: configuration parameters
    :param dataset_names: list of dataset names (e.g. names of the corresponding publications)
    :param dataset_years: list of publication year
    :param dataset_files: list of dataset file path
    """
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
                        Phenotype.objects(sample=s, name=pname). \
                            update_one(set__name=pname, set__phenotype=phenotype,
                                       set__sample=s, set__species=sp,
                                       set__dataset=dt, upsert=True)
                        p = Phenotype.objects(sample=s, name=pname).first()
                        sample.Sample.objects(run_accession=run_accession).update(add_to_set__phenotypes__=p)
                    except errors.ValidationError:
                        continue
                        # print(traceback.format_exc())
