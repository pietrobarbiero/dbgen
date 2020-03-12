import traceback

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


def import_data(species_name: str):
    """
    Import a new species

    Parameters
    ----------
    :param species_name: species name
    """
    try:
        Species.objects(name=species_name).update_one(set__name=species_name, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())
