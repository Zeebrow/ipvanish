import pytest
from pytest import MonkeyPatch
import os
from os.path import expanduser
from pathlib import Path
import random

from ipvanish import ConfigurationSet, Config, get_ovpn_config_dir
#from fixtures.fixt_cfg_dir import fake_cfg_dir
from fixtures.fixt_cfg_dir import fake_cfg_dir

# TODO there's gotta be a better way to do monkeypatching envs...
#monkeypatch = MonkeyPatch()
#monkeypatch.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
def test_CS_country_list_is_sorted(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        unordered_list = []
        for c in os.listdir(cfg_dir):
            unordered_list.append(c)

        previous = None
        for specimen in ipv_config.countries:
            if previous is None:
                previous = specimen
                continue
            assert previous < specimen
            previous = specimen

def test_CS_abv_list_eq_country_list():
    cfg_dir = Path('./select_configfiles')
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m .setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        config = ConfigurationSet()
        assert len(config.cityXcountry) == len(config.abvXcountry)

def test_CS_loads_country_details():
    cfg_dir = Path('./select_configfiles')
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        num_countries = 52 # number of details in constants.py ctry_details dict
        config = ConfigurationSet()
        assert str(cfg_dir) == '/home/builder/app/tests/select_configfiles' 
        assert len(config.country_details.keys()) == num_countries

def test_CS_loads_(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert len(ipv_config.configs) == ovpn_fcount

# TODO need better fixture
def test_CS_cityXcountry(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.cityXcountry

# TODO need better fixture
def test_CS_serverXcity(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.cityXcountry

# TODO need better fixture
def test_CS_serverXabv(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.serverXabv

def test_CS_serverXabv_same_len_as_serverXcity(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        for sxa in ipv_config.serverXabv:
            for sxc in ipv_config.serverXcity:
                
                print(f"{len(ipv_config.serverXabv[sxa])=} == {len(ipv_config.serverXcity[sxc])=}")
                assert len(ipv_config.serverXabv[sxa]) == len(ipv_config.serverXcity[sxc])

def test_get_countries(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)

def test_file_data_hash():
    pass


if __name__ == '__main__':
    cfg_dir = get_ovpn_config_dir()
    cs = ConfigurationSet(cfg_dir)
    for i in cs.cityXcountry:
        print(f"{i} ({len(cs.cityXcountry[i])}): {', '.join(cs.cityXcountry[i])}")
    for i in cs.abvXcountry:
        print(f"{i} ({len(cs.abvXcountry[i])}): {', '.join(cs.abvXcountry[i])}")
    for i in cs.serverXcity:
        print(f"{i} ({len(cs.serverXcity[i])}): {', '.join(cs.serverXcity[i])}")
    for abv in cs.serverXabv:
        print(f"{abv} ({len(cs.serverXabv[abv])}): {', '.join(cs.serverXabv[abv])}")

    

