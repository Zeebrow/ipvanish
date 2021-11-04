import pytest
from pytest import MonkeyPatch
from ipvanish import ConfigurationSet
from fixt_cfg_dir import fixture_config_dirs

import os

@pytest.fixture
def patched_cs(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    monkeypatch = MonkeyPatch()
    with monkeypatch.context() as m:
        m.setenv("IPVANISH_CONFIG_DIR", str(cfg_dir))
        ipv_config = ConfigurationSet(cfg_dir)

    return cfg_dir


def test_patched_cs(fixture_config_dirs):
    cfg_dir, ovpn_fcount = fixture_config_dirs
    for i in range(5):
        cf = ConfigurationSet(cfg_dir)
        print(cf.cfg_dir)
        print(os.listdir(cf.cfg_dir))



if __name__ == '__main__':
    pass
