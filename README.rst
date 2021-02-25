databricks-dbapi
================

|pypi| |pyversions|

.. |pypi| image:: https://img.shields.io/pypi/v/databricks-dbapi.svg
    :target: https://pypi.python.org/pypi/databricks-dbapi

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/databricks-dbapi.svg
    :target: https://pypi.python.org/pypi/databricks-dbapi

A thin wrapper around `pyhive <https://github.com/dropbox/PyHive>`__ and `pyodbc <https://github.com/mkleehammer/pyodbc>`__ for creating a `DBAPI <https://www.python.org/dev/peps/pep-0249/>`__ connection to Databricks Workspace and SQL Analytics clusters. SQL Analytics clusters require the `Simba ODBC driver <https://databricks.com/spark/odbc-driver-download>`__.

Also provides a SQLAlchemy Dialect for Databricks Workspace clusters.

Installation
------------

Install using pip:

.. code-block:: bash

    pip install databricks-dbapi


For SQLAlchemy support install with:

.. code-block:: bash

    pip install databricks-dbapi[sqlalchemy]

Usage
-----

PyHive
~~~~~~

The ``connect()`` function returns a ``pyhive`` Hive connection object, which internally wraps a ``thrift`` connection.

Connecting with ``http_path``, ``host``, and a ``token``:

.. code-block:: python

    import os

    from databricks_dbapi import hive


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    http_path = os.environ["DATABRICKS_HTTP_PATH"]


    connection = hive.connect(
        host=host,
        http_path=http_path,
        token=token,
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM some_table LIMIT 100")

    print(cursor.fetchone())
    print(cursor.fetchall())


The ``pyhive`` connection also provides async functionality:

.. code-block:: python

    import os

    from databricks_dbapi import hive
    from TCLIService.ttypes import TOperationState


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    cluster = os.environ["DATABRICKS_CLUSTER"]


    connection = hive.connect(
        host=host,
        cluster=cluster,
        token=token,
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM some_table LIMIT 100", async_=True)

    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
        logs = cursor.fetch_logs()
        for message in logs:
            print(message)

        # If needed, an asynchronous query can be cancelled at any time with:
        # cursor.cancel()

        status = cursor.poll().operationState

    print(cursor.fetchall())


ODBC
~~~~

The ODBC DBAPI requires the Simba ODBC driver.

Connecting with ``http_path``, ``host``, and a ``token``:

.. code-block:: python

    import os

    from databricks_dbapi import odbc


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    http_path = os.environ["DATABRICKS_HTTP_PATH"]


    connection = odbc.connect(
        host=host,
        http_path=http_path,
        token=token,
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM some_table LIMIT 100")

    print(cursor.fetchone())
    print(cursor.fetchall())


SQLAlchemy
----------

Once the ``databricks-dbapi`` package is installed, the ``databricks+pyhive`` dialect/driver will be registered to SQLAlchemy. Fill in the required information when passing the engine URL.

.. code-block:: python

    from sqlalchemy import *
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import *


    engine = create_engine(
        "databricks+pyhive://token:<databricks_token>@<host>:<port>/<database>",
        connect_args={"http_path": "<cluster_http_path>"}
    )

    logs = Table("my_table", MetaData(bind=engine), autoload=True)
    print(select([func.count("*")], from_obj=logs).scalar())


Refer to the following documentation for more details on hostname, cluster name, and http path:

* `Databricks <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`__
* `Azure Databricks <https://docs.azuredatabricks.net/user-guide/bi/jdbc-odbc-bi.html>`__


Related
-------

* `pyhive <https://github.com/dropbox/PyHive>`__
* `thrift <https://github.com/apache/thrift/tree/master/lib/py>`__
* `pyodbc <https://github.com/mkleehammer/pyodbc>`__
