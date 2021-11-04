import unittest
import pytest
from pytest import MonkeyPatch
from pathlib import Path
from ipvanish import Config, ConfigurationSet
from fixtures.fixt_cfg_dir import fake_cfg_dir

# TODO convert to pytest
def test_Config_repr(fake_cfg_dir):
    cfg_dir=fake_cfg_dir
    pass

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
        # catch dashes
        self.assertEqual(gc2.country, "US")
        self.assertEqual(gc2.city, "San-Jose")
        self.assertEqual(gc2.city_short, "sjc")
        self.assertEqual(gc2.server, "a54")

    def test_city_invalid_file_ext_rasises(self):
        with self.assertRaises(OSError):
            Config(self.badname1)
    
    


