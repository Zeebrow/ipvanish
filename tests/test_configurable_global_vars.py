import pytest
from pytest import MonkeyPatch
from os.path import expanduser
from pathlib import Path
from ipvanish import get_ovpn_config_dir, list_configs#, city_abv_pair
import random
import tempfile
import os
from fixtures.fixt_cfg_dir import fake_cfg_dir

#cwd = Path(os.path.dirname(__file__))
#config_testdata = str(cwd / "empty_confgfiles")
#default_config_dir = str(Path( os.path.expanduser('~')) / ".config/ipvanish/configs")

# TODO: change name of func from list_configs() to list_configs()
def test_list_configs_is_configurable(fake_cfg_dir):
    cfg_dir, ovpn_fcount = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        cfg_list = list_configs(cfg_dir)
        assert len(cfg_list) == ovpn_fcount

def test_default_config_dir_is_user_dotconfig(fake_cfg_dir):
    cfg_dir, _ = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.delenv("IPVANISH_CONFIG_DIR", raising=False)
        m.delenv("XDG_CONFIG_HOME", raising=False)
        assert get_ovpn_config_dir(str(cfg_dir)) == str(cfg_dir)

def test_IPVANISH_CONFIG_DIR_overrides_XDG(fake_cfg_dir):
    default_xdg_config_home =  str(Path( expanduser('~')) / ".config")
    cfg_dir, _ = fake_cfg_dir
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        m.setenv("XDG_CONFIG_HOME", default_xdg_config_home)
        assert get_ovpn_config_dir() != str(Path( default_xdg_config_home ) / "ipvanish/configs")
        assert get_ovpn_config_dir() == str(cfg_dir)

def test_IPVANISH_CONFIG_DIR_overrides_XDG(fake_cfg_dir):
    default_xdg_config_home =  str(Path( expanduser('~')) / ".config")
    cfg_dir, _ = fake_cfg_dir
    tempdir = tempfile.mkdtemp()
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        m.setenv("XDG_CONFIG_HOME", default_xdg_config_home)
        cf = get_ovpn_config_dir(tempdir)
        assert len(os.listdir(cf)) == 0
        #assert get_ovpn_config_dir() != str(Path( default_xdg_config_home ) / "ipvanish/configs")
        #assert get_ovpn_config_dir() == str(cfg_dir)

def test_cli_arg_overrides_IPVANISH_CONFIG_DIR():
    pass

#def test_city_abv_pair(fake_cfg_dir):
#    cfg_dir, _ = fake_cfg_dir
#    monkeypatch = MonkeyPatch()
#    with monkeypatch.context() as m:
#        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
#        len(city_abv_pair())


        
if __name__ == '__main__':
    pytest.main(['--trace',__file__])
