import argparse

import pandas as pd
from mongoengine import QuerySet

from ..tables import species, dataset


def _load_configuration() -> argparse.Namespace:
    """
    Parse command line arguments.

    Parameters
    ----------
    :return: configuration object
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="Password for running mongo.", required=False)
    parser.add_argument("-s", "--species", help="Species name.", required=False, default="Species 1")
    parser.add_argument("--species-dir", help="Species directory.", required=False, default="./test/data/species1")
    parser.add_argument("-f", "--fastq-dir", help="Root directory where fastq sample files will be stored.",
                        required=False, default="./test/data/db/raw")
    parser.add_argument("-d", "--dataset", help="Dataset to add.", required=False, default="all")
    args = parser.parse_args()

    return args


def _options(queryset: QuerySet, species_name: str = None, dataset_name: str = None, phenotype_name: str = None):
    """
    Filter query according to the provided parameters

    :param queryset: current objects to be filtered
    :param species_name: species name
    :param dataset_name: dataset name
    :param phenotype_name: phenotype name
    """
    if species_name and phenotype_name and dataset_name:
        s = species.Species.objects(name=species_name).first()
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(species=s, dataset=d, name=phenotype_name)

    elif species_name and dataset_name and (not phenotype_name):
        s = species.Species.objects(name=species_name).first()
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(species=s, dataset=d)

    elif (not species_name) and phenotype_name and dataset_name:
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(dataset=d, name=phenotype_name)

    elif species_name and phenotype_name and (not dataset_name):
        s = species.Species.objects(name=species_name).first()
        data = queryset.filter(species=s, name=phenotype_name)

    elif species_name and (not phenotype_name) and (not dataset_name):
        s = species.Species.objects(name=species_name).first()
        data = queryset.filter(species=s)

    elif dataset_name and (not phenotype_name) and (not species_name):
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(dataset=d)

    else:
        return pd.DataFrame()

    return data
