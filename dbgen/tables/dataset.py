import traceback
from argparse import Namespace
from typing import List

from mongoengine import Document, StringField, IntField, ListField, ReferenceField, errors

from . import species
from . import sample


class Dataset(Document):
    """
    Dataset

    Attributes
    ----------
    :param name: name (e.g. name of the corresponding publication)
    :param area: geographic area
    :param year: publication year
    :param samples: list of sample IDs belonging to the dataset
    """
    name = StringField(max_length=200, unique=True)
    area = StringField(max_length=200)
    year = IntField()
    samples = ListField(ReferenceField(sample.Sample))


def import_data(species_name: str, dataset_name: str, dataset_year: str):
    """
    Import dataset

    Parameters
    ----------
    :param species_name: species name
    :param dataset_name: dataset names (e.g. name of the corresponding publication)
    :param dataset_year: publication year
    """
    try:
        Dataset.objects(name=dataset_name).update_one(set__name=dataset_name, set__year=dataset_year, upsert=True)
        d = Dataset.objects(name=dataset_name).first()
        species.Species.objects(name=species_name).update(add_to_set__datasets__=d)
    except errors.ValidationError:
        print(traceback.format_exc())
