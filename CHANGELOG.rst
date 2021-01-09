Release History
---------------

0.4.0: 2021-01-09
~~~~~~~~~~~~~~~~~

* Override get_columns in DatabricksDialect to account for differences in Databricks and OSS Hive partition header
* Fix version file
* Update black and add isort
* Add org id argument for connection


0.3.0: 2019-08-14
~~~~~~~~~~~~~~~~~

* Add module globals to make DBAPI PEP 249 compliant
* Allow port and database name to be passed in connect function
* Add compatibility with SQLAlchemy

0.2.0: 2018-12-12
~~~~~~~~~~~~~~~~~

* Add docstring
* Add http_path parameter for Azure compatibility (thanks @gwerbin)
* Make metadata available at package level

0.1.1: 2018-10-10
~~~~~~~~~~~~~~~~~

* Fix email

0.1.0: 2018-09-10
~~~~~~~~~~~~~~~~~

* First release