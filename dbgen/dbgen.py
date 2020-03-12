from argparse import Namespace

from mongoengine import connect

from .utils import _load_configuration, _load_sources
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


def connect_db(configs: Namespace):
    """
    Connect to default database

    Parameters
    ----------
    :param configs: configuration parameters
    """
    db = connect(configs.database, host=configs.host, port=configs.port)


def shutdown_db(configs: Namespace):
    """
    Shutdown mongoDB service

    Parameters
    ----------
    :param configs: configuration parameters
    """
    mongo_shutdown(configs)


def drop_db(configs):
    """
    Drop default database

    Parameters
    ----------
    :param configs: configuration parameters
    """
    db = connect(configs.database, host=configs.host, port=configs.port)
    db.drop_database(configs.database)


def import_data(configs: Namespace):
    """
    Import data

    Parameters
    ----------
    :param configs: configuration parameters
    """
    _load_sources(configs)


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
