import sqlite3
from pathlib import Path
import re
import hashlib
import os

from .exceptions import InvalidConfigurationWarning 
from .utils import get_ovpn_config_dir

DEFAULT_DB_FILE = str(Path)


class IpvDB:
    def __init__(self, db=None):
        self.cfg_dir = get_ovpn_config_dir()
        if db is None:
            self.db = ':memory:'
        else:
            self.db = db


    def init_db(self):
        """
        primary key is <country>_<city_short>_<server>
        country
        city
        city_short
        server
        """

        conn = sqlite3.connect(self.db)
        curr = conn.cursor()
        cmd_create_ipv_filename_index = "CREATE TABLE IF NOT EXISTS ipv_config_filename (pkey TEXT, country TEXT, city TEXT, abv TEXT, server TEXT, filename TEXT)"
        # cmd_create_server_stats = "CREATE TABLE IF NOT EXISTS server_stats (pkey TEXT, ping INTEGER, last_updated )"
        curr.execute(cmd_create_ipv_filename_index)


    def load_config_files(self, cfg_files: list):
        cmd_populate = "INSERT INTO ipv_config_filename VALUES (?, ?, ?, ?, ?, ?)"
        for C in cfg_files:
            pk = f"{C.country}_{C.city_short}_{C.server}"
            row = (pk, C.country, C.city, C.city_short, C.server, C.fname)
            curr.execute(cmd_populate, row)
            conn.commit()
        conn.close()

    def load(self):
        files = os.listdir(self.cfg_dir)
        for f in files:
            try:
                 self.configs.append(Config(f))
            except OSError:
                pass
        self.init_db()
        print(self.db)
