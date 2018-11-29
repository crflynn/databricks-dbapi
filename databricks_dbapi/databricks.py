""" Create a Hive connection to a Databricks cluster """
import base64
import sys
import warnings

PY2 = sys.version_info[0] < 3

if PY2:
    from urlparse import urlunsplit
else:
    from urllib.parse import urlunsplit

from pyhive import hive
from thrift.transport import THttpClient

__all__ = ('connect',)


def base64_encode_str(s):
    if PY2:
        return base64.standard_b64encode(s)
    else:
        return base64.standard_b64encode(s.encode()).decode()


def connect(hostname, cluster=None, http_path=None, http_path=None, token=None, username=None, password=None, user=None):
    """ Create a Hive connection to a Databricks cluster

    For documentation of the Hive connection itself, see Pyhive: https://github.com/dropbox/PyHive
    
    Parameters
    ----------
    hostname : str
        Hostname of the cluster ("https://" will be prepended)
    cluster : str
        Cluster name, or Cluster ID as found in the Cluster Configuration page; must be None if "http_path" is given
    http_path : str
        The full "HTTP Path" as found in the Cluster Configuration page; must be None if "cluster" is given (use this if "cluster" throws an error)
    token : str
        Databricks access token (strongly preferred to username and password)
    username : str
        Databricks username; ignored if "token" is given, and must be present if "token" is not given
    password : str
        Databricks password; ignored if "token" is given, and must be present if "token" is not given
    user : str
        Deprecated alias for "username"
    """
    if user is not None:
        warnings.warn('"user" argument is deprecated; use "username" instead', DeprecationWarning)
        username = user

    if token is not None:
        if username is not None or password is not None:
            warnings.warn('"token" was given; "username" and "password" will be ignored')
        username = "token"
        password = token
    elif user is None or password is None:
        raise ValueError('Missing arguments. Must provide either "token" or "username"/"password".')

    if cluster is not None:
        if http_path is None:
            http_path = "sql/protocolv1/o/0/%s" % cluster
        else:
            warnings.warn('"http_path" was given; "cluster" will be ignored')
    elif http_path is None:
        raise ValueError('Missing arguments. Must provide either "http_path" or "cluster".')

    auth = "%s:%s" % (username, password)
    url = urlunsplit(("https://", "%s:443" % hostname, http_path, "", ""))

    transport = THttpClient.THttpClient(url)
    transport.setCustomHeaders({"Authorization": "Basic %s" % base64_encode_str(auth)})
    return hive.connect(thrift_transport=transport)
