import pytest
import random

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

