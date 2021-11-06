import pytest
import os

from fixtures.fixt_cfg_dir import fake_cfg_dir, fake_filled_cfg_dir
from ipvanish import ConfigFile, InvalidConfigurationWarning

#TODO
#def test_ConfigFile_rasises_ICW_on_bad_filename():
#    some_file = 'ipvanish-AE-Dubai-dxb-c02.ovpn'
#    with pytest.raises(FileNotFoundError):
#        cf = ConfigFile(some_file)

def test_ConfigFile_rasises_FileNotFound_on_missing_file(fake_filled_cfg_dir):
    cfg_dir, valid_cfg_filecount = fake_filled_cfg_dir
    with pytest.raises(InvalidConfigurationWarning):
        for cfgf in os.listdir(cfg_dir):
            cf = ConfigFile(str(cfgf))

def test_ConfigFile_loads_correctly(fake_filled_cfg_dir):
    cfg_dir, valid_cfg_filecount = fake_filled_cfg_dir
    valid_cfgfs = []
    try:
        for cfgf in os.listdir(cfg_dir):
            valid_cfgfs.append(ConfigFile(str(cfgf)))
    except InvalidConfigurationWarning:
        pass


