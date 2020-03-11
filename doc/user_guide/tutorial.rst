Tutorial
========

DBGen is a general purpose database to support genomic data anlysis studies.
The current implementation is based on mongoDB.


Environment setup
-----------------

In order to use this package, you need to download, install, and
configure mongoDB on your machine.
You can follow the instructions on the official
`website <https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb.>`__.


Configure DBGen
--------------------

DBGen can be easily configured using command line parameters.
There are 4 user parameters:

* ``--password``: the (user) password to access the database
* ``--species``: the name of the species the user wants to access
* ``--species-dir``: the path to the source directory of the species
* ``--dataset``: a specific dataset to add to the database (not required)

You can load the configuration parameters directly in python using the provided method
that will return an ``argparse.Namespace`` object:

.. code:: python

    import dbgen

    configs = dbgen.load_cfg()

The ``configs`` object will be required by other DBGen methods to update the database.


Start and stop MongoDB
-------------------------

DBGen provides two methods to start and stop the MongoDB service
``dbgen.start_db`` and ``dbgen.shutdown_db``:

.. code:: python

    import dbgen

    configs = dbgen.load_cfg()
    dbgen.start_db(configs)
    ...
    dbgen.shutdown(configs)

