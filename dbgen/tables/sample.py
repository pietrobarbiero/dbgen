from mongoengine import Document, StringField, ListField

class Sample(Document):
    run_accession = StringField(max_length=200, primary_key=True)
    download_urls = ListField(StringField(max_length=200))
    fastq_directory = StringField(max_length=200)
