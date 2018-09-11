"""Provide an function to create a Hive connection to a Databricks cluster."""
import base64
import sys

from pyhive import hive
from thrift.transport import THttpClient


PY_MAJOR = sys.version_info[0]


def connect(host, cluster, token=None, user=None, password=None):
    if token is not None:
        auth = "token:%s" % token
    elif user is not None and password is not None:
        auth = "%s:%s" % (user, password)
    else:
        raise ValueError(
            "Missing arguments. Must provide either token or user/password."
        )

    if PY_MAJOR < 3:
        auth = base64.standard_b64encode(auth)
    else:
        auth = base64.standard_b64encode(auth.encode()).decode()

    url = "https://%s:443/sql/protocolv1/o/0/%s" % (host, cluster)

    transport = THttpClient.THttpClient(url)
    transport.setCustomHeaders({"Authorization": "Basic %s" % auth})

    return hive.connect(thrift_transport=transport)
