import unittest
try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

from pyticketswitch.api_exceptions import BackendCallFailure
from pyticketswitch.parse import availability_options_result, discount_options_result


class BackendCallFailureTestCase(unittest.TestCase):

    def test_availability_options_result(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
        <availability_options_result><backend_call_failed/></availability_options_result>
        """
        with self.assertRaises(BackendCallFailure):
            availability_options_result(xml.fromstring(content))

    def test_discount_options_result(self):
        content = """<?xml version="1.0" encoding="UTF-8"?>
        <discount_options_result><backend_call_failed/></discount_options_result>
        """
        with self.assertRaises(BackendCallFailure):
            discount_options_result(xml.fromstring(content))
