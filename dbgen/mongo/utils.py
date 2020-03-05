import os


def mongo_status(configs):
    command = 'sudo service mongod status'
    p = os.system('echo %s | sudo -S %s' % (configs.password, command))
    return p


def mongo_start(configs):
    command = 'sudo service mongod start'
    p = os.system('echo %s | sudo -S %s' % (configs.password, command))
    return p


def mongo_shutdown(configs):
    command = 'sudo service mongod stop'
    p = os.system('echo %s | sudo -S %s' % (configs.password, command))
    return p