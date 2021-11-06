import pytest
from pathlib import Path
from os import listdir
from fixtures.fixt_cfg_dir import create_config_filename, fixture_config_dirs
from fixtures.data import some_52_countries

def test_create_config_filename_rtns_different_files_each_call():
    for i in range(5):
        set1 = create_config_filename()
        set2 = create_config_filename()
        print(f"{set1} != {set2}? ")
        assert set1 != set2

def test_create_config_filename_country_position():
    countries = ['AB', 'BC', 'CD', 'DN', 'US']
    #countries = some_52_countries
    for c in countries:
        cfname = create_config_filename(country=c)
        print(f"{c} == {cfname.split('-')[1]}?")
        assert cfname.split('-')[1] == c

def test_create_config_filename_sity_position():
    cities = ['Atlanta', 'Birmingham', 'Deez-Nutz', 'Chicago', 'New-Delhi']
    for c in cities:
        cfname = create_config_filename(city=c)
        print(f"{c} in {cfname}?")
        print(f"{c} == ('{cfname.split('-')[2]}' or '{'-'.join(cfname.split('-')[2:4])}')?")
        assert ((cfname.split('-')[2] == c) or ('-'.join(cfname.split('-')[2:4]) == c))

def test_create_config_filename_abv_position():
    abvs = ['atl', 'ham', 'ntz', 'chi', 'ned']
    for c in abvs:
        cfname = create_config_filename(abv=c)
        print(f"{c} == {cfname.split('-')[-2]}?")
        assert cfname.split('-')[-2] == c

def test_create_config_filename_server_position():
    servers = ['a01', 'a11', 'b03', 'c69', 'a34']
    for c in servers:
        cfname = create_config_filename(server=c)
        print(f"{c} in {cfname}?")
        assert cfname.split('-')[-1].split('.')[0] == c


# --------------------- fixture_config_dirs() ---------------------------

def test_fixture_config_dirs_rtn_types():
    cfg_dir, good_filecount = fixture_config_dirs()
    assert type(cfg_dir) == type(Path())
    assert type(good_filecount) == type(int())
    
    fixt_cfg_dirs = fixture_config_dirs()
    assert type(fixt_cfg_dirs) == type(('a','b'))

def test_fixture_config_dir_makes_files():
    cfg_dir, good_filecount = fixture_config_dirs()
    assert listdir(cfg_dir) is not None










