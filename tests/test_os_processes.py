import pytest
from ipvanish import import_config
from fixtures.fixt_cfg_dir import fake_cfg_dir

def test_import_config_raises_FileNotFound():
    with pytest.raises(FileNotFoundError):
        import_config('asdfasdfasdfasdf')
        