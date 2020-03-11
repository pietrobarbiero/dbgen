from argparse import Namespace

from mongoengine import connect

from .utils import _load_configuration, parse_ast
from .mongo import mongo_start, mongo_shutdown
from .tables import species, dataset, sample, phenotype


def load_cfg() -> Namespace:
    """
    Load configuration parameters

    :return: configuration parameters
    """
    return _load_configuration()


def start_db(configs: Namespace):
    """
    Start mongoDB service

    Parameters
    ----------
    :param configs: configuration parameters
    """
    mongo_start(configs)


def connect_db():
    """
    Connect to default database
    """
    db = connect('dbgen_test', host='localhost', port=27017)


def shutdown_db(configs: Namespace):
    """
    Shutdown mongoDB service

    Parameters
    ----------
    :param configs: configuration parameters
    """
    mongo_shutdown(configs)


def drop_db():
    """
    Drop default database
    """
    db = connect('dbgen_test', host='localhost', port=27017)
    db.drop_database('dbgen_test')


def import_data(configs: Namespace):
    """
    Import data

    Parameters
    ----------
    :param configs: configuration parameters
    """
    # parse phenotype
    dataset_names, dataset_years, dataset_files = parse_ast(configs)

    # import data
    species.import_data(configs)
    dataset.import_data(configs, dataset_names, dataset_years, dataset_files)
    sample.import_data(configs, dataset_names, dataset_years, dataset_files)
    phenotype.import_data(configs, dataset_names, dataset_years, dataset_files)


def print_db():
    """
    Print default database
    """
    for s in species.Species.objects:
        print("%s (%d)" % (s.name, len(s.datasets)))
        for dref in s.datasets:
            d = dataset.Dataset.objects(pk=dref.id).first()
            if d is not None:
                print("\t%s (%d)" % (d.name, len(d.samples)))
                for sref in d.samples:
                    s = sample.Sample.objects(pk=sref.id).first()
                    if s is not None:
                        phenotypes = ["{%s: %s}" % (p.name, p.phenotype) for p in s.phenotypes]
                        print("\t\t%s %s" % (s.run_accession, phenotypes))
