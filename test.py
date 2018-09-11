import os

from databricks_dbapi import databricks


token = os.environ["DATABRICKS_TOKEN"]

user = os.environ["DATABRICKS_USER"]
password = os.environ["DATABRICKS_PASSWORD"]

host = os.environ["DATABRICKS_HOST"]
cluster = os.environ["DATABRICKS_CLUSTER"]


def token_test():
    connection = databricks.connect(host=host, cluster=cluster, token=token)
    cursor = connection.cursor()
    print(cursor)


def user_password_test():
    connection = databricks.connect(
        host=host, cluster=cluster, user=user, password=password
    )
    cursor = connection.cursor()
    print(cursor)


if __name__ == "__main__":
    token_test()
    user_password_test()
