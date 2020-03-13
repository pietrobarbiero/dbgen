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


Documentation
--------------

Documentation for the
`latest stable version <https://dbgen.readthedocs.io/en/latest/>`__
is available on ReadTheDocs.


Running tests
-------------

You can run all unittests from command line by using python:

.. code:: bash

    $ python -m unittest discover

or coverage:

.. code:: bash

    $ coverage run -m unittest discover


Contributing
------------

Please read the
`contributing section <https://github.com/pietrobarbiero/dbgen/blob/master/doc/user_guide/contributing.rst>`__
for details on our code of conduct, and the process for submitting pull requests to us.


Authors
-------

`Pietro Barbiero <http://www.pietrobarbiero.eu/>`__, Computational Scientist.

Licence
-------

Copyright 2020 Pietro Barbiero.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.