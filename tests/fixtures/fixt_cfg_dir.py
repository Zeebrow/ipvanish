import pytest
from pytest import MonkeyPatch
import random
import string
from collections import defaultdict

import tempfile
import os
from pathlib import Path
from ipvanish import ConfigurationSet

def create_config_filename(namelen=10, **kw) -> string:
    """
    kwargs:  country city, abv
    """ 
    for k in kw.keys():
        if k not in ['country', 'city', 'abv', 'server']:
            print(f"WARN: ignoring keyword argument '{k}'")
            continue
    c,a = city_abv_pair(city_name_len=namelen)
    return f"ipvanish-{kw.get('country', 'US')}-{kw.get('city',c)}-{kw.get('abv',a)}-{kw.get('server', random_server_name())}.ovpn"

def ascii(num=1, case=None) -> str:
    """
    Generate random ascii characters of definite length, or in a pattern
    """
    if case in ('u', 'upper'):
        _f = lambda: random.choice(string.ascii_uppercase)
    elif case in ('l', 'lower'):
        _f = lambda: random.choice(string.ascii_lowercase)
    elif case in ('p', 'proper'):
        _f = lambda: random.choice(string.ascii_lowercase)
        return random.choice(string.ascii_uppercase) + ''.join([_f() for i in range(num-1)])
    else:
        _f = lambda: random.choice(string.ascii_letters)
    return ''.join([_f() for i in range(num)])

def srvr_digits(num=2) -> str:
    if num < 1:
        raise ValueError("number of digits must be greater than 0")
    return "%02d" % random.randint(0, 9*(10**(num-1)))

def city_abv_pair(city_name_len=10) -> tuple:
    name = ascii(city_name_len, 'proper')
    abv = name[0:2].lower() + name[-1]
    return name,abv

def random_server_name():
    return ascii(1,'l') + srvr_digits(2)

#@pytest.fixture
def fixture_config_dirs(tmp_path='', range_lo=5, range_hi=10):
    """
    returns a tuple of the path to a temporary directory and the randomly
    generated number of empty .ovpn files inside.
    """
    tdir = Path(tempfile.TemporaryDirectory().name)
    #tdir = tmp_path / "configs"
    tdir.mkdir()
    num_files = random.randint(range_lo,range_hi)
    for f in range(num_files):
        f1 = tdir / f"file{f}.ovpn"
        f1 = tdir / create_config_filename()
        f1.touch()
    # make some other files too
    for i in range(random.randint(1,3)):
        randofile = tdir/f"rando{i}"
        randofile.touch()

    return (tdir, num_files)

@pytest.fixture
def fake_cfg_dir():
    return fixture_config_dirs()

@pytest.fixture
def patched_cs():
    cfg_dir, ovpn_count = fixture_config_dirs()
    print(os.listdir(cfg_dir))
    mp = MonkeyPatch()
    with mp.context() as mc:
        rtn = ConfigurationSet(cfg_dir)
        return (rtn, cfg_dir, ovpn_count)

def test_patched_cs(patched_cs):
    cf, cfg, ct = patched_cs
    assert os.listdir(cfg) == os.listdir(cf.cfg_dir)

    print(f"TEST_PATCHED_CS: {cf.countries}")
    print(f"TEST_PATCHED_CS: {cfg}")
    print(f"TEST_PATCHED_CS: {cf.cfg_dir}")

if __name__ == '__main__':
    for i in range(5):
        gf, ct = fixture_config_dirs()
        for j in os.listdir(gf):
            print(f"({i}) {j}")

    # sanity checks
#    print()
#    print(f"{ascii(2,'l')=}")
#    print(f"{ascii(2,'u')=}")
#    print(f"{ascii(10,'p')=}")
#    print()
#    print(f"{create_config_filename(namelen=15, country='US')=}")
#    print(f"{create_config_filename(country='US')=}")
#    print(f"{create_config_filename(city='Abbudabi')=}")
#    print(f"{create_config_filename(abv='adb')=}")
#    print(f"{create_config_filename(server='a01')=}")
#    print()
#    print(f"{srvr_digits(1)=}")
#    print(f"{srvr_digits(2)=}")
#    print()
#    print(f"{city_abv_pair()=}")
#    print(f"{city_abv_pair(15)=}")
#    print()
#    print(f"{random_server_name()=}")
#    print()
#    print(f"{create_config_filename()=}")
#    print(f"{create_config_filename(5)=}")
#    print(f"{create_config_filename(15)=}")
#    print(f"{create_config_filename(20)=}")
#
