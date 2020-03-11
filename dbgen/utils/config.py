import argparse


def load_configuration() -> argparse.Namespace:
    """
    Load run parameters from .ini configuration file.

    Parameters
    ----------
    :return: configuration object
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="Password for running mongo.", required=False)
    parser.add_argument("-s", "--species", help="Species name.", required=False, default="Staphylococcus Aureus")
    parser.add_argument("--species-dir", help="Species directory.", required=False, default="./test/data/species1")
    parser.add_argument("-f", "--fastq-dir", help="Root directory where fastq sample files will be stored.",
                        required=False, default="./test/data/db/raw")
    parser.add_argument("-d", "--dataset", help="Dataset to add.", required=False, default="all")
    args = parser.parse_args()

    return args
