import pytest
from pytest import MonkeyPatch
import os
from os.path import expanduser
from pathlib import Path
import random

from ipvanish import ConfigurationSet, Config, get_ovpn_config_dir
from fixtures.fixt_cfg_dir import fixture_config_dirs

def test_CS_country_list_is_sorted(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
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




def test_CS_loads_(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert len(ipv_config.configs) == ovpn_fcount

# TODO need better fixture
def test_CS_cityXcountry(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.cityXcountry

# TODO need better fixture
def test_CS_serverXcity(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.cityXcountry

# TODO need better fixture
def test_CS_serverXabv(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        assert ipv_config.serverXabv

def test_CS_serverXabv_same_len_as_serverXcity(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)
        for sxa in ipv_config.serverXabv:
            for sxc in ipv_config.serverXcity:
                assert len(ipv_config.serverXabv[sxa]) == len(ipv_config.serverXcity[sxc])

def test_get_countries(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)




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

    

