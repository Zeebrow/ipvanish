import unittest
from ipvanish import Config

class TestFilenameParsing(unittest.TestCase):

    def setUp(self):
        self.goodname1 = 'ipvanish-US-Seattle-sea-a30.ovpn'
        self.goodname2 = 'ipvanish-US-San-Jose-sjc-a54.ovpn'
        self.badname1 = 'ipvanish-US-Seattle-sea-a30.ovpnx'

    def test_city_params_parse_correctly(self):
        gc1 = Config(self.goodname1)
        gc2 = Config(self.goodname2)
        self.assertEqual(gc1.country, "US")
        self.assertEqual(gc1.city, "Seattle")
        self.assertEqual(gc1.city_short, "sea")
        self.assertEqual(gc1.server, "a30")
        # careful to catch dashes
        self.assertEqual(gc2.country, "US")
        self.assertEqual(gc2.city, "San-Jose")
        self.assertEqual(gc2.city_short, "sjc")
        self.assertEqual(gc2.server, "a54")

    def test_city_invalid_file_ext_rasises(self):
        with self.assertRaises(OSError):
            Config(self.badname1)

