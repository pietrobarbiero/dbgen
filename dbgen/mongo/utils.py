import os
import traceback
from argparse import Namespace


def mongo_start(configs: Namespace):
    """
    Start mongoDB service

    Parameters
    ----------
    :param configs: configuration parameters
    """
    if configs.password:
        try:
            command = 'sudo service mongod start'
            p = os.system('echo %s | sudo -S %s' % (configs.password, command))
            return p
        except:
            print(traceback.format_exc())


def mongo_shutdown(configs: Namespace):
    """
    Shutdown mongoDB service

    Parameters
    ----------
    :param configs: configuration parameters
    """
    if configs.password:
        try:
            command = 'sudo service mongod stop'
            p = os.system('echo %s | sudo -S %s' % (configs.password, command))
            return p
        except:
            print(traceback.format_exc())
