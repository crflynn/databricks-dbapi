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


Related
-------

* `pyhive <https://github.com/dropbox/PyHive>`_
* `thrift <https://github.com/apache/thrift/tree/master/lib/py>`_