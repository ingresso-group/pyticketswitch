from vcr_unittest import VCRTestCase

from .. import settings_test as settings


class InterfaceObjectTestCase(VCRTestCase):
    api_settings = {
        'username': settings.TEST_USERNAME,
        'password': settings.TEST_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }

    def _get_vcr_kwargs(self):
        kwargs = super(InterfaceObjectTestCase, self)._get_vcr_kwargs()
        # We need to match queries based on the request body since all
        # specifics of the call are in the body
        kwargs['match_on'] = ['uri', 'query', 'headers', 'raw_body']
        return kwargs


class InterfaceObjectCreditUserTestCase(InterfaceObjectTestCase):
    api_settings = {
        'username': settings.TEST_CREDIT_USERNAME,
        'password': settings.TEST_CREDIT_PASSWORD,
        'url': settings.API_URL,
        'ext_start_session_url': settings.EXT_START_SESSION_URL
    }
