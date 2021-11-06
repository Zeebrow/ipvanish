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
    with pytest.raises(FileNotFoundError):
        for cfgf in os.listdir(cfg_dir):
            #_cf = Config(Path(cfg_dir)/cfgf)
            #cf = _cf.config_file
            cf = ConfigFile(str(cfgf))

def test_ConfigFile_loads_correctly(fake_filled_cfg_dir):
    cfg_dir, valid_cfg_filecount = fake_filled_cfg_dir
    valid_cfgfs = []
    try:
        for cfgf in os.listdir(cfg_dir):
            #_cf = Config(Path(cfg_dir)/cfgf)
            #valid_cfgfs.append(_cf.config_file)
            #valid_cfgfs.append(ConfigFile(str(cfgf)))
            cf = ConfigFile(str(cfg_dir/cfgf))
    except InvalidConfigurationWarning:
        pass


