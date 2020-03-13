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
There are 5 user parameters:

* ``--password``: user password
* ``--database``: database name (default: ``dbgen_test``)
* ``--host``: host name (default: ``localhost``)
* ``--port``: port (default: ``27017``)
* ``--root-data-dir``: root directory for input data (default: ``./test/data``)


You can load the configuration parameters directly in python using DBGen.
The method ``load_cfg`` will return an object of class ``argparse.Namespace``:

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


DBGen database
---------------------

The database schema of DBGen is composed of 5 tables:

* ``Species``: the basic unit of classification and a taxonomic rank of an organism
* ``Dataset``: an homogeneous collection of organisms' samples
* ``Sample``: collected individuals
* ``Phenotype``: observable characteristics of a sample
* ``Result``: output result of bioinformatic tools

.. image:: database.png


Load data
----------------

Once you have loaded the configuration parameters and started the database service,
you are ready to upload data into DBGen.

In order to simplify the insertion of new information, DBGen is designed to scan a user-defined
directory looking for new data. The pre-defined directory is ``./test/data``. You can change
the default directory using the command line parameter ``--root-data-dir``.

In order to work properly, DBGen requires a specific tree structure under
the root data directory:


.. code-block:: text

    root-data-dir
    |
    +-- <species name>
    |   +-- <year>_<publicationName>.txt
    |   +-- <year>_<publicationName>.txt
    |   +-- ...
    |
    +-- <species name>
    |   +-- <year>_<publicationName>.txt
    |   +-- ...
    +-- ...

Each text file must be formatted as following:

+------------------+-----------------------------------------------------------------+-------------------+-----------------+-----------------+-----+
| **Project name** | **URLs**                                                        | **Run accession** | **Phenotype A** | **Phenotype B** | ... |
+------------------+-----------------------------------------------------------------+-------------------+-----------------+-----------------+-----+
| PRJNA497094      | ftp.baz/SRR8074810_1.fastq.gz;ftp.baz/SRR8074810_2.fastq.gz     | SRR8074810        | R               | S               |     |
+------------------+-----------------------------------------------------------------+-------------------+-----------------+-----------------+-----+
| PRJNA497094      | ftp.baz/SRR8074811_1.fastq.gz;ftp.baz/SRR8074811_2.fastq.gz     | SRR8074811        | R               | S               |     |
+------------------+-----------------------------------------------------------------+-------------------+-----------------+-----------------+-----+

