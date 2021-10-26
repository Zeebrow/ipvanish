import pytest
from pytest import MonkeyPatch
import os
import tempfile
from pathlib import Path
from ipvanish import get_ovpn_config_dir, get_configs

cwd = Path(os.path.dirname(__file__))
config_testdata = str(cwd / "empty_confgfiles")
default_config_dir = str(Path( os.path.expanduser('~')) / ".config/ipvanish/configs")
default_xdg_config_home =  str(Path( os.path.expanduser('~')) / ".config")

def test_default_config_dir_is_user_dotconfig():
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.delenv("IPVANISH_CONFIG_DIR", raising=False)
        m.delenv("XDG_CONFIG_HOME", raising=False)
        assert get_ovpn_config_dir(default_configs_dir=config_testdata) == config_testdata

def test_IPVANISH_CONFIG_DIR_overrides_XDG():
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", config_testdata)
        m.setenv("XDG_CONFIG_HOME", default_xdg_config_home)
        assert get_ovpn_config_dir() != str(Path( default_xdg_config_home ) / "ipvanish/configs")
        assert get_ovpn_config_dir() == config_testdata

def test_cli_arg_overrides_IPVANISH_CONFIG_DIR():
    pass

def test_get_configs():
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", config_testdata)
        cfg_list = get_configs()
    assert len(cfg_list) == 1962
        

