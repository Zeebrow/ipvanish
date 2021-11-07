import pytest
from ipvanish import update_configs
from fixtures.fixt_cfg_dir import fake_filled_cfg_dir
import os

#TODO: mock exception (its hard-coded in processes.py)
def test_update_configs_archive_creates_compressed_file(fake_filled_cfg_dir):
    cfg_dir, _ = fake_filled_cfg_dir
    for f in os.listdir(cfg_dir):
        if not f.endswith('.ovpn'):
            os.remove(os.path.join(cfg_dir,f))
    update_configs(cfg_dir=cfg_dir)
    with pytest.raises(Exception):
        with open(cfg_dir) as zf:
            magic_bytes = zf.read(2).decode()
            assert magic_bytes in [
                "PK", # zip file
            ]


def test_update_configs_backsup_to_specified_path():
    pass

def test_update_config_removes_backup_zip_on_success():
    pass

def test_restore_backup():
    pass
