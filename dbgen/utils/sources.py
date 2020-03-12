import json
import os
from argparse import Namespace
from typing import Tuple, List

from ..tables import dataset, species, sample, phenotype


def _load_sources(configs: Namespace):
    """
    Parse phenotype files

    Parameters
    ----------
    :param configs: configuration parameters
    """
    for species_name in os.listdir(configs.root_data_dir):
        species_dir_path = os.path.join(configs.root_data_dir, species_name)
        print(species_dir_path)
        if os.path.isdir(species_dir_path):
            for dataset_file in os.listdir(species_dir_path):
                dataset_file_path = os.path.join(species_dir_path, dataset_file)
                if os.path.isfile(dataset_file_path):
                    print("\t" + dataset_file_path)
                    dataset_name = str(dataset_file).split(".txt")[0]
                    if not dataset.Dataset.objects(name=dataset_name):
                        dataset_abs_path = os.path.abspath(dataset_file_path)
                        dataset_year = json.loads(dataset_name.split("_")[0])
                        species.import_data(species_name)
                        dataset.import_data(species_name, dataset_name, dataset_year)
                        sample.import_data(species_name, dataset_name, dataset_abs_path)
                        phenotype.import_data(species_name, dataset_name, dataset_abs_path)
