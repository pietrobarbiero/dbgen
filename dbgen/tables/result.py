from mongoengine import Document, StringField, DateTimeField, FileField


class Result(Document):
    """
    Result

    Attributes
    ----------
    :param tool: bioinformatic tool name
    :param version: bioinformatic tool version
    :param date: date when the result has been collected
    :param parameters: bioinformatic tool parameters
    :param raw_result: raw result provided by the bioinformatic tool
    """
    tool = StringField(max_length=200, unique_with=["version", "parameters"])
    version = StringField(max_length=200, unique_with=["tool", "parameters"])
    date = DateTimeField()
    parameters = StringField(max_length=200, unique_with=["tool", "version"])
    raw_result = FileField()
