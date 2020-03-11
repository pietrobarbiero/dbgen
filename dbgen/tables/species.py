import traceback
from argparse import Namespace

from mongoengine import Document, StringField, ListField, ReferenceField, errors, queryset_manager

from .dataset import Dataset


class Species(Document):
    """
    Species

    Attributes
    ----------
    :param name: name
    :param datasets: list of references to datasets related to the species
    """
    name = StringField(max_length=200, unique=True)
    datasets = ListField(ReferenceField(Dataset))


def import_data(configs: Namespace):
    """
    Import a new species

    Parameters
    ----------
    :param configs: configuration parameters
    """
    try:
        Species.objects(name=configs.species).update_one(set__name=configs.species, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())
