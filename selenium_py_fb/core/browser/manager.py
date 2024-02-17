import logging
import pickle
import random
import time
from pathlib import Path
from typing import (
    Any,
    Literal,
)

import selenium.webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_py_fb.core.browser.likes_struct import LikesEsEnum

logger: logging.Logger = logging.getLogger(__name__)


class BrowserFB:
    driver: selenium.webdriver.Chrome
    """
    Selenium driver for webbroser to use
    """
    webdriver_options: Options
    """
    Options for selenium webdriver
    """
    cookies_dir: Path
    """
    dir where stores cookies for webdrivers
    """
    accounts_db: dict[str, dict[str, str]]

    def __init__(
        self,
        cookies_dir: Path,
        accounts_db: dict[str, Any],
        run_mode: Literal["background"] | Literal["foreground"] = "background",
    ):
        self.cookies_dir = cookies_dir
        self.session_cookies_dir = Path(
            cookies_dir,
            "facebook",
        )

        self.accounts_db = accounts_db
        self.__init_driver(
            run_mode=run_mode,
        )

    def __init_driver(
        self,
        run_mode: Literal["background"] | Literal["foreground"],
    ):
        self.webdriver_options = Options()

        # Clean browser
        self.webdriver_options.add_argument("--disable-infobars")
        self.webdriver_options.add_argument("--disable-extensions")

        # Disable Pop alerts
        self.webdriver_options.add_experimental_option(
            "prefs",
            {"profile.default_content_setting_values.notifications": 1},
        )

        # Case Foreground
        if run_mode == "foreground":
            self.webdriver_options.add_argument("start-maximized")

        # Case background
        if run_mode == "background":
            self.webdriver_options.add_argument("--headless")
            # Supress background logs
            self.webdriver_options.add_argument("--log-level=3")

    def start_web_driver(self):
        self.driver = selenium.webdriver.Chrome(
            options=self.webdriver_options,
        )

    def get_session_cookie_path(
        self,
        email_alias: str,
        profile_id: str,
    ):
        return Path(self.session_cookies_dir, email_alias, f"{profile_id}.pkl")

    def load_session(self, email_alias: str, profile_id: str):
        self.driver.get("https://www.facebook.com/")
        with open(self.get_session_cookie_path(email_alias=email_alias, profile_id=profile_id), "rb") as _fread:
            cookies = pickle.load(_fread)

        # Delete old case
        self.driver.delete_all_cookies()

        # Add the cookies to the driver
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # Refresh the page to apply the cookies
        self.driver.refresh()

    def do__like(
        self,
        post_url: str,
        like_type: LikesEsEnum = LikesEsEnum.LOVE,
    ):
        self.driver.get(post_url)
        actions = ActionChains(self.driver)
        actions.move_to_element(
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{LikesEsEnum.LIKE}']"))
            )
        ).perform()
        self.wait()
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@aria-label='{like_type}']"))
        ).click()
        self.wait()

    def do__like_all(
        self,
        post_url: str,
        like_type: LikesEsEnum = LikesEsEnum.LOVE,
    ):
        for email_alias_i, profiles_i in self.accounts_db.items():
            for profile_id_i, profile_name_i in profiles_i.items():
                retries = 0
                while retries < 3:
                    try:
                        logger.debug(
                            f"Cargando session de\nprofile_id: {profile_id_i}\nprofile_name: {profile_name_i}"
                        )
                        self.load_session(email_alias=email_alias_i, profile_id=profile_id_i)
                        self.wait()
                        self.do__like(post_url=post_url, like_type=like_type)
                        self.wait()
                        break
                    except TimeoutException:
                        logger.warning("##### Bypass by timeout #####")
                        pass
                    retries += 1
                    logger.debug(f"Retry... {retries}")

    @staticmethod
    def wait():
        time.sleep(random.uniform(0.5, 3.0))
