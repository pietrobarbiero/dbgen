import json
import os


def parse_ast(configs):
    dataset_names = []
    dataset_years = []
    dataset_files = []
    for f in os.listdir(configs.species_dir):
        rel_path = os.path.join(configs.species_dir, f)
        if os.path.isfile(rel_path) and rel_path.endswith("_AST.txt"):
            dataset_files.append(os.path.abspath(rel_path))
            dataset_names.append(f.split("_AST")[0])
            dataset_years.append(json.loads(f.split("_")[2]))
    return dataset_names, dataset_years, dataset_files
