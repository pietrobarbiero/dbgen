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
    :param sample: reference to the corresponding sample
    :param dataset: reference to the corresponding dataset
    :param species: reference to the corresponding species
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
    def get_phenotype_names(doc_cls, queryset: QuerySet, species_name=None, dataset_name=None) -> Set:
        """
        Get all phenotype names available

        :param species_name: name of the species
        :param dataset_name: name of the dataset
        """
        data = _options(queryset, species_name, dataset_name)
        names = set()
        for d in data:
            names.add(d.name)
        return names


def _to_df(ph: Phenotype):
    d = {ph.sample.pk: (ph.species.name, ph.dataset.name, ph.phenotype)}
    df = pd.DataFrame.from_dict(d, orient="index", columns=["species", "dataset", ph.name])
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
        for i, (pname, phenotype) in enumerate(row.items()):
            if i > 2:
                try:
                    s = sample.Sample.objects(project=project, run_accession=run_accession).first()
                    sp = species.Species.objects(name=species_name).first()
                    dt = dataset.Dataset.objects(name=dataset_name).first()
                    Phenotype.objects(sample=s, name=pname). \
                        update_one(set__name=pname, set__phenotype=phenotype,
                                   set__sample=s, set__species=sp,
                                   set__dataset=dt, upsert=True)
                    p = Phenotype.objects(sample=s, name=pname).first()
                    sample.Sample.objects(project=project, run_accession=run_accession).update(add_to_set__phenotypes__=p)
                except errors.ValidationError:
                    continue
                    # print(traceback.format_exc())
