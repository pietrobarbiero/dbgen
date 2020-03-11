import traceback

from mongoengine import Document, StringField, IntField, ListField, ReferenceField, errors

from . import species
from . import sample


class Dataset(Document):
    name = StringField(max_length=200, unique=True)
    area = StringField(max_length=200)
    year = IntField()
    samples = ListField(ReferenceField(sample.Sample))


def import_data(configs, dataset_names, dataset_years, dataset_files):
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        try:
            Dataset.objects(name=dname).update_one(set__name=dname, set__year=dyear, upsert=True)
            d = Dataset.objects(name=dname).first()
            species.Species.objects(name=configs.species).update(add_to_set__datasets__=d)
        except errors.ValidationError:
            print(traceback.format_exc())
