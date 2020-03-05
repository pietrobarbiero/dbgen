from mongoengine import Document, StringField, ListField, ReferenceField

from dbgen.tables.dataset import Dataset


class Species(Document):
    name = StringField(max_length=200, primary_key=True)
    # datasets = EmbeddedDocumentListField(Dataset, default=[])
    datasets = ListField(ReferenceField(Dataset))

    # @queryset_manager
    # def objects(doc_cls, queryset):
    #     return queryset.order_by('-name')
