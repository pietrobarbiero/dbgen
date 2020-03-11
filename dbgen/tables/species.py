import traceback

from mongoengine import Document, StringField, ListField, ReferenceField, errors, queryset_manager

from .dataset import Dataset


class Species(Document):
    name = StringField(max_length=200, unique=True)
    datasets = ListField(ReferenceField(Dataset))


def import_data(configs):
    try:
        Species.objects(name=configs.species).update_one(set__name=configs.species, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())
