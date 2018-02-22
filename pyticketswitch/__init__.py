import json
from os.path import dirname
from pyticketswitch.client import Client  # NOQA


with open('{}/pkg_info.json'.format(dirname(__file__))) as fp:
    __pkg_info__ = json.load(fp)

__version__ = __pkg_info__['version']
