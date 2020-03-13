DBGen - General purpose database for genomic data analysis
=============================================================


|Build|
|Coverage|

|PyPI license|
|PyPI-version|



.. |Build| image:: https://img.shields.io/travis/pietrobarbiero/dbgen?label=Master%20Build&style=for-the-badge
    :alt: Travis (.org)
    :target: https://travis-ci.org/pietrobarbiero/dbgen

.. |Coverage| image:: https://img.shields.io/codecov/c/gh/pietrobarbiero/dbgen?label=Test%20Coverage&style=for-the-badge
    :alt: Codecov
    :target: https://codecov.io/gh/pietrobarbiero/dbgen

.. |Docs| image:: https://img.shields.io/readthedocs/pietrobarbiero/dbgen?style=for-the-badge
    :alt: Read the Docs (version)
    :target: https://dbgen.readthedocs.io/en/latest/

.. |PyPI license| image:: https://img.shields.io/pypi/l/dbgen.svg?style=for-the-badge
   :target: https://pypi.python.org/pypi/dbgen/

.. |PyPI-version| image:: https://img.shields.io/pypi/v/dbgen?style=for-the-badge
    :alt: PyPI
    :target: https://pypi.python.org/pypi/dbgen/



DBGen is a python package providing a general purpose database
to support genomic data analysis studies.

The current implementation is based on mongoDB.


Quick start
-----------

You can install DBGen along with all its dependencies from
`PyPI <https://pypi.org/project/dbgen/>`__:

.. code:: bash

    $ pip install -r requirements.txt dbgen

Source
------

The source code and minimal working examples can be found on
`GitHub <https://github.com/pietrobarbiero/dbgen>`__.


.. toctree::
    :caption: User Guide
    :maxdepth: 2

    user_guide/installation
    user_guide/tutorial
    user_guide/contributing
    user_guide/running_tests

.. toctree::
    :caption: API Reference
    :maxdepth: 2

    modules/dbgen
    modules/tables/species
    modules/tables/dataset
    modules/tables/sample
    modules/tables/phenotype
    modules/tables/result


.. toctree::
    :caption: Copyright
    :maxdepth: 1

    user_guide/authors
    user_guide/licence


Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`