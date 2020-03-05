from mongoengine import Document, StringField, IntField, ListField, ReferenceField

from dbgen.tables.sample import Sample


class Dataset(Document):
    name = StringField(max_length=200, primary_key=True)
    area = StringField(max_length=200)
    year = IntField()
    samples = ListField(ReferenceField(Sample))
