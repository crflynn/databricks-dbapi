from sqlalchemy import create_engine


def test_sqlalchemy_workspace(token_workspace, host, http_path_workspace, odbc_driver_path):
    engine = create_engine(
        f"databricks+pyodbc://token:{token_workspace}@{host}:443/default",
        connect_args={"http_path": f"{http_path_workspace}", "driver_path": odbc_driver_path},
    )
    connection = engine.connect()
    print(connection)


def test_sqlalchemy_sql_analytics(token_sql_analytics, host, http_path_sql_analytics, odbc_driver_path):
    engine = create_engine(
        f"databricks+pyodbc://token:{token_sql_analytics}@{host}:443/default",
        connect_args={"http_path": f"{http_path_sql_analytics}", "driver_path": odbc_driver_path},
    )
    connection = engine.connect()
    print(connection)
