import unittest

from .. import settings_test as settings


class InterfaceObjectTestCase(unittest.TestCase):
    api_settings = {
        'username': settings.TEST_USERNAME,
        'password': settings.TEST_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }


class InterfaceObjectCreditUserTestCase(unittest.TestCase):
    api_settings = {
        'username': settings.TEST_CREDIT_USERNAME,
        'password': settings.TEST_CREDIT_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }
