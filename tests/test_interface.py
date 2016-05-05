from __future__ import absolute_import
import pytest
from pyticketswitch.interface import CoreAPI
from pyticketswitch.core_objects import RunningUser

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml


@pytest.fixture
def valid_start_session_result():
    raw = """<?xml version="1.0" encoding="UTF-8"?>
        <start_session_result>
          <subdomain_user_is_bad>no</subdomain_user_is_bad>
          <crypto_block>abc123</crypto_block>
          <running_user>
            <backend_group>tsw</backend_group>
            <default_country_code>uk</default_country_code>
            <default_lang_code>en</default_lang_code>
            <is_b2b>no</is_b2b>
            <real_name>Demonstration User</real_name>
            <style>pure</style>
            <user_id>demo</user_id>
          </running_user>
          <country_code>uk</country_code>
          <country_desc>United Kingdom</country_desc>
        </start_session_result>
    """
    result = xml.fromstring(raw)
    return result


@pytest.fixture
def core():
    core = CoreAPI(
        username='demo',
        password='demopass',
        url='http://api.ticketswitch.com/tickets/xml_core.exe',
        remote_ip='123.123.123.123',
        remote_site='demotickets.com',
        accept_language='en',
        api_request_timeout=10,
    )
    return core


def test_core_api_start_session(core, monkeypatch, valid_start_session_result):

    def fake_call(*args, **kwargs):
        return valid_start_session_result

    monkeypatch.setattr(core, '_create_xml_and_post', fake_call)

    result = core.start_session()

    assert result == 'abc123'
    assert core.running_user is not None
    assert core.running_user.user_id == 'demo'


def test_core_api_start_session_with_custom_start_session_method(core):

    def fake_start_session_method(remote_ip, remote_site):
        assert remote_ip == '123.123.123.123'
        assert remote_site == 'demotickets.com'
        return {
            'crypto_block': '123abc',
            'user_id': 'demo',
            'running_user': RunningUser(
                user_id='demo',
                style='pure',
            )
        }

    core.custom_start_session = fake_start_session_method

    result = core.start_session()

    assert result == '123abc'
    assert core.username == 'demo'
    assert core.running_user is not None
    assert core.running_user.user_id == 'demo'
