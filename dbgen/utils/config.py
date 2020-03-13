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
    parser.add_argument("-p", "--password", help="Password to access the DB service.", required=False)
    parser.add_argument("--database", help="Database name.", required=False, default="dbgen_test")
    parser.add_argument("--host", help="Host.", required=False, default="localhost")
    parser.add_argument("--port", help="Port.", required=False, default=27017)
    parser.add_argument("-r", "--root-data-dir", help="Root directory for input data.",
                        required=False, default="./test/data/")
    args = parser.parse_args()

    return args


def _options(queryset: QuerySet, species_name: str = None, dataset_name: str = None, pheno_or_tool_name: str = None):
    """
    Filter query according to the provided parameters

    :param queryset: current objects to be filtered
    :param species_name: species name
    :param dataset_name: dataset name
    :param pheno_or_tool_name: phenotype name
    """
    if species_name and pheno_or_tool_name and dataset_name:
        s = species.Species.objects(name=species_name).first()
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(species=s, dataset=d, name=pheno_or_tool_name)

    elif species_name and dataset_name and (not pheno_or_tool_name):
        s = species.Species.objects(name=species_name).first()
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(species=s, dataset=d)

    elif (not species_name) and pheno_or_tool_name and dataset_name:
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(dataset=d, name=pheno_or_tool_name)

    elif species_name and pheno_or_tool_name and (not dataset_name):
        s = species.Species.objects(name=species_name).first()
        data = queryset.filter(species=s, name=pheno_or_tool_name)

    elif species_name and (not pheno_or_tool_name) and (not dataset_name):
        s = species.Species.objects(name=species_name).first()
        data = queryset.filter(species=s)

    elif dataset_name and (not pheno_or_tool_name) and (not species_name):
        d = dataset.Dataset.objects(name=dataset_name).first()
        data = queryset.filter(dataset=d)

    else:
        return pd.DataFrame()

    return data
