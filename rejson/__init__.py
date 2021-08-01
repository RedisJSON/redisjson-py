import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("redisjson").version
except:
    __version__ = "99.99.99"  # developing
from .client import Client
from .path import Path
