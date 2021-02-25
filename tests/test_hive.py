from databricks_dbapi import hive


def test_workspace(host, http_path_workspace, token_workspace):
    connection = hive.connect(host=host, http_path=http_path_workspace, token=token_workspace)
    cursor = connection.cursor()
    print(cursor)
