import traceback

from mongoengine import Document, StringField, DateTimeField, FileField


class Result(Document):
    tool = StringField(max_length=200, unique_with=["version", "parameters"])
    version = StringField(max_length=200, unique_with=["tool", "parameters"])
    date = DateTimeField()
    parameters = StringField(max_length=200, unique_with=["tool", "version"])
    raw_result = FileField()
