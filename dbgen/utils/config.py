import argparse


def load_configuration() -> argparse.Namespace:
    """
    Load run parameters from .ini configuration file.

    Parameters
    ----------
    :param config_path: configuration file path
    :param config_file: configuration file name
    :return: configuration object
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="Password for running mongo.", required=True)
    parser.add_argument("-t", "--task", help="Task to perform.", required=True,
                        default="import", choices=['import', 'export', 'query'])
    parser.add_argument("-s", "--species", help="Species name.", required=False, default="Staphylococcus Aureus")
    parser.add_argument("--species-dir", help="Species directory.", required=False, default="./bacteria/staphylococcus-aureus")
    parser.add_argument("-d", "--dataset", help="Dataset to add.", required=False, default="all")
    args = parser.parse_args()

    return args
