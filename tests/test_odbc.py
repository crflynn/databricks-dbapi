from databricks_dbapi import odbc


def test_workspace(host, http_path_workspace, token_workspace, odbc_driver_path):
    connection = odbc.connect(
        host=host, http_path=http_path_workspace, token=token_workspace, driver_path=odbc_driver_path
    )
    cursor = connection.cursor()
    print(cursor)


def test_sql_analytics(host, http_path_sql_analytics, token_sql_analytics, odbc_driver_path):
    connection = odbc.connect(
        host=host, http_path=http_path_sql_analytics, token=token_sql_analytics, driver_path=odbc_driver_path
    )
    cursor = connection.cursor()
    print(cursor)
