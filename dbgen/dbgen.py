from mongoengine import connect

from .utils import load_configuration, parse_ast
from .mongo import mongo_start, mongo_shutdown
from .tables import species, dataset, sample, phenotype


def load_cfg():
    return load_configuration()


def start_db(configs):
    mongo_start(configs)
    return configs


def connect_db():
    db = connect('dbgen_test', host='localhost', port=27017)


def shutdown_db(configs):
    mongo_shutdown(configs)


def drop_db():
    db = connect('dbgen_test', host='localhost', port=27017)
    db.drop_database('dbgen_test')


def import_data(configs):
    # parse phenotype
    dataset_names, dataset_years, dataset_files = parse_ast(configs)

    # import data
    species.import_data(configs)
    dataset.import_data(configs, dataset_names, dataset_years, dataset_files)
    sample.import_data(configs, dataset_names, dataset_years, dataset_files)
    phenotype.import_data(configs, dataset_names, dataset_years, dataset_files)
    return


def print_db():
    for s in species.Species.objects:
        print("%s (%d)" % (s.name, len(s.datasets)))
        for dref in s.datasets:
            d = dataset.Dataset.objects(pk=dref.id).first()
            if d is not None:
                print("\t%s (%d)" % (d.name, len(d.samples)))
                for sref in d.samples:
                    s = sample.Sample.objects(pk=sref.id).first()
                    if s is not None:
                        phenotypes = ["{%s: %s}" % (p.name, p.phenotype) for p in s.phenotypes]
                        print("\t\t%s %s" % (s.run_accession, phenotypes))
