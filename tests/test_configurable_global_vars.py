import pytest
from pytest import MonkeyPatch
import os
import tempfile
from pathlib import Path
from ipvanish import get_ovpn_config_dir, list_configs
import random

cwd = Path(os.path.dirname(__file__))
config_testdata = str(cwd / "empty_confgfiles")
#default_config_dir = str(Path( os.path.expanduser('~')) / ".config/ipvanish/configs")
default_xdg_config_home =  str(Path( os.path.expanduser('~')) / ".config")

@pytest.fixture
def fixture_config_dirs(tmp_path, range_lo=5, range_hi=10):
    """
    returns a tuple of the path to a temporary directory and the randomly
    generated number of empty .ovpn files inside.
    """
    #tdir = tempfile.TemporaryDirectory()
    tdir = tmp_path / "configs"
    tdir.mkdir()
    num_files = random.randint(range_lo,range_hi)
    for f in range(num_files):
        f1 = tdir / f"file{f}.ovpn"
        f1.touch()
    # make some other files too
    for i in range(random.randint(1,3)):
        randofile = tdir/f"rando{i}"
        randofile.touch()
    
    return (tdir, num_files)

# TODO: change name of func from list_configs() to list_configs()
def test_list_configs_is_configurable(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        cfg_list = list_configs(cfg_dir)
        assert len(cfg_list) == ovpn_fcount

def test_default_config_dir_is_user_dotconfig(fixture_config_dirs):
    cfg_dir, _ = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.delenv("IPVANISH_CONFIG_DIR", raising=False)
        m.delenv("XDG_CONFIG_HOME", raising=False)
        assert get_ovpn_config_dir(str(cfg_dir)) == str(cfg_dir)

def test_IPVANISH_CONFIG_DIR_overrides_XDG():
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", config_testdata)
        m.setenv("XDG_CONFIG_HOME", default_xdg_config_home)
        assert get_ovpn_config_dir() != str(Path( default_xdg_config_home ) / "ipvanish/configs")
        assert get_ovpn_config_dir() == config_testdata

def test_cli_arg_overrides_IPVANISH_CONFIG_DIR():
    pass

def test_list_configs():
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", config_testdata)
        cfg_list = list_configs()
    assert len(cfg_list) == 1962
        
if __name__ == '__main__':
    pytest.main(['--trace',__file__])
