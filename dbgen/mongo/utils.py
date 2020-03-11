import os
import traceback


def mongo_start(configs):
    if configs.password:
        try:
            command = 'sudo service mongod start'
            p = os.system('echo %s | sudo -S %s' % (configs.password, command))
            return p
        except:
            print(traceback.format_exc())


def mongo_shutdown(configs):
    if configs.password:
        try:
            command = 'sudo service mongod stop'
            p = os.system('echo %s | sudo -S %s' % (configs.password, command))
            return p
        except:
            print(traceback.format_exc())
