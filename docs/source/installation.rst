Installation
============

The Python SDK supports fault tolerant and multi-threaded programming support.

It also supports docker and K8s elastic, load balancing too.

Python Version
--------------

We recommend using the latest version of Python. This SDK supports
Python 3.6 and newer.


Dependencies
------------

Cryptonets-SDK has dependencies on numpy, scipy and Pillow for image processing.
These distributions will be installed automatically. PrivateID will
detect and use them if already installed.

* `Numpy`_ provides functions for array wise image manipulation.
* `Pillow`_ provides functionalities for reading the Image and converting to required formats.

.. _Numpy: https://pypi.org/project/numpy/
.. _Pillow: https://pypi.org/project/Pillow/

Virtual environments
--------------------

We recommend you use a virtual environment to manage the dependencies for your project,
both in development and in production.

What problem does a virtual environment solve? The more Python
projects you have, the more likely it is that you need to work with
different versions of Python libraries, or even Python itself. Newer
versions of libraries for one project can break compatibility in
another project.

Virtual environments are independent groups of Python libraries, one for
each project. Packages installed for one project will not affect other
projects or the operating system's packages.

Python comes bundled with the :mod:`venv` module to create virtual
environments.


Create an environment
~~~~~~~~~~~~~~~~~~~~~

Create a project folder and a :file:`venv` folder within:

.. code-block:: sh

    mkdir myproject
    cd myproject
    python3 -m venv venv

On Windows:

.. code-block:: bat

    py -3 -m venv venv


Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before you work on your project, activate the corresponding environment:

.. code-block:: sh

    . venv/bin/activate

On Windows:

.. code-block:: bat

    venv\Scripts\activate

Your shell prompt will change to show the name of the activated
environment.

.. _installation:

Install Cryptonets SDK
----------------------

Within the activated environment, use the following command to install:

.. code-block:: sh

    pip3 install cryptonets_python_sdk

Upgrade Cryptonets SDK
----------------------

To upgrade the cryptonets SDK version, use the following command:

.. code-block:: sh

    pip3 install --upgrade --no-cache cryptonets_python_sdk
