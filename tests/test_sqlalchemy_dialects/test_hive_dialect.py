from sqlalchemy import create_engine


def test_sqlalchemy_workspace(token_workspace, host, http_path_workspace):
    engine = create_engine(
        f"databricks+pyhive://token:{token_workspace}@{host}:443/default",
        connect_args={"http_path": f"{http_path_workspace}"},
    )
    connection = engine.connect()
    print(connection)
