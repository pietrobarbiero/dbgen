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


def import_data(configs: Namespace, dataset_names: List, dataset_years: List, dataset_files: List):
    """
    Import new datasets

    Parameters
    ----------
    :param configs: configuration parameters
    :param dataset_names: list of dataset names (e.g. names of the corresponding publications)
    :param dataset_years: list of publication year
    :param dataset_files: list of dataset file path
    """
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        try:
            Dataset.objects(name=dname).update_one(set__name=dname, set__year=dyear, upsert=True)
            d = Dataset.objects(name=dname).first()
            species.Species.objects(name=configs.species).update(add_to_set__datasets__=d)
        except errors.ValidationError:
            print(traceback.format_exc())
