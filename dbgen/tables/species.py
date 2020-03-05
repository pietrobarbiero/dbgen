import traceback

from mongoengine import Document, StringField, ListField, ReferenceField, errors

from .dataset import Dataset


class Species(Document):
    name = StringField(max_length=200, primary_key=True)
    # datasets = EmbeddedDocumentListField(Dataset, default=[])
    datasets = ListField(ReferenceField(Dataset))

    # @queryset_manager
    # def objects(doc_cls, queryset):
    #     return queryset.order_by('-name')


def import_data(configs):
    try:
        Species.objects(name=configs.species).update_one(set__name=configs.species, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())