import os
import sys
from pathlib import Path

# Ensure project packages
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, os.path.abspath(BASE_DIR))

import json
import logging

from selenium_py_fb.core.browser.manager import BrowserFB

logger = logging.getLogger(__name__)

# Config dirs
RUN_DIR = Path(BASE_DIR, "run")
"""
Dir where files for local running are stored
"""
RUN_DIR.mkdir(exist_ok=True)

COOKIES_DIR = Path(RUN_DIR, "cookies")
COOKIES_DIR.mkdir(exist_ok=True)


account_db_pathfile = Path(RUN_DIR, "db.json")
with open(account_db_pathfile, encoding="utf8") as json_file:
    accounts_db = json.load(json_file)


browser = BrowserFB(
    cookies_dir=COOKIES_DIR,
    accounts_db=accounts_db,
    run_mode="background",
)
