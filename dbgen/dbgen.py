import json
import os
import traceback

import pandas as pd
from mongoengine import connect, errors

from .config import load_configuration
from .mongo import mongo_start, mongo_shutdown
from .tables import Dataset, Species, Sample


def print_db():
    for item in Species.objects:
        print("%s (%d)" % (item.name, len(item.datasets)))
        for dref in item.datasets:
            d = Dataset.objects(name=dref.id).first()
            if d is not None:
                print("\t%s (%d)" % (d.name, len(d.samples)))


def import_data(configs):
    # insert tables
    try:
        Species.objects(name=configs.species).update_one(set__name=configs.species, upsert=True)
    except errors.ValidationError:
        print(traceback.format_exc())
    print_db()

    dataset_files = []
    dataset_names = []
    dataset_years = []
    for f in os.listdir(configs.species_dir):
        rel_path = os.path.join(configs.species_dir, f)
        if os.path.isfile(rel_path) and rel_path.endswith("_AST.txt"):
            dataset_files.append(os.path.abspath(rel_path))
            dataset_names.append(f.split("_AST")[0])
            dataset_years.append(json.loads(f.split("_")[2]))

    # insert datasets
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        try:
            Dataset.objects(name=dname).update_one(set__name=dname, set__year=dyear, upsert=True)
            Species.objects(pk=configs.species).update(add_to_set__datasets__=dname)
        except errors.ValidationError:
            print(traceback.format_exc())
    print_db()

    # insert samples
    for dname, dyear, dpath in zip(dataset_names, dataset_years, dataset_files):
        df = pd.read_csv(dpath, sep="\t")
        df.dropna(axis=0, inplace=True, how="all")
        dataset = Dataset.objects(name=dname).first()
        for _, row in df.iterrows():
            run_accession = row[2]
            download_urls = row[1].split(";")
            try:
                Sample.objects(run_accession=run_accession).\
                    update_one(set__run_accession=run_accession, set__download_urls=download_urls, upsert=True)
                Dataset.objects(pk=dname).update(add_to_set__samples__=run_accession)
            except errors.ValidationError:
                print(traceback.format_exc())
    print_db()

    return


def run():
    configs = load_configuration()
    mongo_start(configs)
    db = connect('dbgen_test', host='localhost', port=27017)

    if configs.task == "import":
        import_data(configs)

    # TODO: to be deleted
    # db.drop_database('dbgen_test')

    mongo_shutdown(configs)
    return
