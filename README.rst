databricks-dbapi
================

|pypi| |pyversions|

.. |pypi| image:: https://img.shields.io/pypi/v/databricks-dbapi.svg
    :target: https://pypi.python.org/pypi/databricks-dbapi

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/databricks-dbapi.svg
    :target: https://pypi.python.org/pypi/databricks-dbapi

A thin wrapper around `pyhive <https://github.com/dropbox/PyHive>`_ for creating a `DBAPI <https://www.python.org/dev/peps/pep-0249/>`_ connection to an interactive Databricks cluster.

Also provides a SQLAlchemy Dialect for Databricks interactive clusters.

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

The ``connect()`` function returns a ``pyhive`` Hive connection object, which internally wraps a ``thrift`` connection.

Using a Databricks API token (recommended):

.. code-block:: python

    import os

    from databricks_dbapi import databricks


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    cluster = os.environ["DATABRICKS_CLUSTER"]


    connection = databricks.connect(
        host=host,
        cluster=cluster,
        token=token,
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM some_table LIMIT 100")

    print(cursor.fetchone())
    print(cursor.fetchall())


Using your username and password (not recommended):

.. code-block:: python

    import os

    from databricks_dbapi import databricks


    user = os.environ["DATABRICKS_USER"]
    password = os.environ["DATABRICKS_PASSWORD"]
    host = os.environ["DATABRICKS_HOST"]
    cluster = os.environ["DATABRICKS_CLUSTER"]


    connection = databricks.connect(
        host=host,
        cluster=cluster,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM some_table LIMIT 100")

    print(cursor.fetchone())
    print(cursor.fetchall())


Connecting on Azure platform, or with ``http_path``:

.. code-block:: python

    import os

    from databricks_dbapi import databricks


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    http_path = os.environ["DATABRICKS_HTTP_PATH"]


    connection = databricks.connect(
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

    from databricks_dbapi import databricks
    from TCLIService.ttypes import TOperationState


    token = os.environ["DATABRICKS_TOKEN"]
    host = os.environ["DATABRICKS_HOST"]
    cluster = os.environ["DATABRICKS_CLUSTER"]


    connection = databricks.connect(
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



SQLAlchemy
----------

Once the ``databricks-dbapi`` package is installed, the ``databricks+pyhive`` dialect/driver will be registered to SQLAlchemy. Fill in the required information when passing the engine URL.

.. code-block:: python

    from sqlalchemy import *
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import *


    # Standard Databricks with user + password: provide user, password, company name for url, database name, cluster name
    engine = create_engine("databricks+pyhive://<user>:<password>@<companyname>.cloud.databricks.com:443/<database>", connect_args={"cluster": "<cluster>"})

    # Standard Databricks with token: provide token, company name for url, database name, cluster name
    engine = create_engine("databricks+pyhive://token:<databricks_token>@<companyname>.cloud.databricks.com:443/<database>", connect_args={"cluster": "<cluster>"})

    # Azure Databricks with user + password: provide user, password, region for url, database name, http_path (with cluster name)
    engine = create_engine("databricks+pyhive://<user>:<password>@<region>.azuredatabricks.net:443/<database>", connect_args={"http_path": "<azure_databricks_http_path>"})

    # Azure Databricks with token: provide token, region for url, database name, http_path (with cluster name)
    engine = create_engine("databricks+pyhive://token:<databrickstoken>@<region>.azuredatabricks.net:443/<database>", connect_args={"http_path": "<azure_databricks_http_path>"})


    logs = Table("my_table", MetaData(bind=engine), autoload=True)
    print(select([func.count("*")], from_obj=logs).scalar())


Refer to the following documentation for more details on hostname, cluster name, and http path:

* `Databricks <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`_
* `Azure Databricks <https://docs.azuredatabricks.net/user-guide/bi/jdbc-odbc-bi.html>`_


Related
-------

* `pyhive <https://github.com/dropbox/PyHive>`_
* `thrift <https://github.com/apache/thrift/tree/master/lib/py>`_