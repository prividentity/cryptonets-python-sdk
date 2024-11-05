Installation Guide
==================

The CryptoNets™ Python SDK is designed to support fault-tolerant, multi-threaded programming, as well as containerized environments.
It is compatible with Docker and Kubernetes, enabling elastic scaling and load balancing for optimal performance.

Supported Python Versions
-------------------------

We recommend using the latest version of Python. This SDK supports Python 3.6 and newer.

Dependencies
------------
CryptoNets™ SDK relies on a few key libraries for image processing, which will be installed automatically.
If these libraries are already present, the SDK will detect and use them:

* `Numpy`_ Provides essential functions for array-based image manipulation.
* `Pillow`_ Offers functionalities for reading and converting images to required formats.

.. _Numpy: https://pypi.org/project/numpy/
.. _Pillow: https://pypi.org/project/Pillow/

Using Virtual Environments
--------------------------

We recommend using a virtual environment to manage dependencies for your project, both in development and production.
Virtual environments help you avoid conflicts between different project dependencies, as each environment isolates the required libraries and Python versions.

Python includes the built-in :mod:`venv` module, which allows you to create virtual environments easily.

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a project folder and a :file:`venv` folder within it:

.. code-block:: sh

    mkdir myproject
    cd myproject
    python3 -m venv venv

On Windows:

.. code-block:: bat

    py -3 -m venv venv


Activating the Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

Before working on your project, activate the virtual environment:

.. code-block:: sh

    . venv/bin/activate

On Windows:

.. code-block:: bat

    venv\Scripts\activate

Your shell prompt will change to indicate that the environment is activated.

.. _installation:

Installing CryptoNets™ SDK
--------------------------

Once the environment is activated, install the SDK with the following command:

.. code-block:: sh

    pip3 install cryptonets_python_sdk

Upgrading CryptoNets™ SDK
-------------------------

To upgrade to the latest version of the CryptoNets™ SDK, use:

.. code-block:: sh

    pip3 install --upgrade --no-cache cryptonets_python_sdk

By following these steps, you'll ensure a seamless setup for developing with the CryptoNets™ Python SDK.