import traceback

from mongoengine import Document, StringField, ListField, ReferenceField, errors, queryset_manager

from .dataset import Dataset


class Species(Document):
    name = StringField(max_length=200, primary_key=True)
    datasets = ListField(ReferenceField(Dataset))

    @queryset_manager
    def get_by_name(doc_cls, queryset, species_name):
        return queryset.filter(name=species_name).first()

    @queryset_manager
    def get_dataset(doc_cls, queryset, species_name, dataset_name):
        sp = doc_cls.get_by_name(species_name)
        for dataset in sp.datasets:
            if dataset.name == dataset_name:
                return dataset


def import_data(configs):
    try:
        Species.objects(name=configs.species).update_one(set__name=configs.species, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())
