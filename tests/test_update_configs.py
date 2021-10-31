import pytest
from ipvanish import update_configs

def test_update_configs_archive_creates_compressed_file():
    update_configs()
