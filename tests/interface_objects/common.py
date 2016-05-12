# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from vcr_unittest import VCRTestCase

from .. import settings_test as settings

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml


def xml_matcher(r1, r2):
    """ Match requests by Core XML API method name """
    r1_xml = xml.fromstring(r1.body)
    r2_xml = xml.fromstring(r2.body)
    return r1_xml.tag == r2_xml.tag


class InterfaceObjectTestCase(VCRTestCase):
    api_settings = {
        'username': settings.TEST_USERNAME,
        'password': settings.TEST_PASSWORD,
        'url': settings.API_URL,
    }

    def _get_vcr(self):
        myvcr = super(InterfaceObjectTestCase, self)._get_vcr()
        myvcr.register_matcher('xml_matcher', xml_matcher)
        myvcr.match_on = ['xml_matcher']
        return myvcr


class InterfaceObjectCreditUserTestCase(InterfaceObjectTestCase):
    api_settings = {
        'username': settings.TEST_CREDIT_USERNAME,
        'password': settings.TEST_CREDIT_PASSWORD,
        'url': settings.API_URL,
    }
