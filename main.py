from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# from selenium.common.exceptions import ElementClickInterceptedException
from dotenv import load_dotenv

import time
import os
import random
import logging

from logger_config import log_error
from loop import user_loop

load_dotenv(override=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
MESSAGE = os.getenv("MESSAGE")
FILE = os.getenv("FILE")


class InstaFollower:
    def __init__(self):
        self.close_notis = False
        brave_path = "/usr/bin/brave-browser"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = brave_path
        chrome_options.add_experimental_option("detach", True)
        # Activar el modo headless
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        try:
            # post url
            url = "https://www.instagram.com"
            self.driver.get(url)
            time.sleep(random.uniform(4, 7))

            # Check id the cookie warning is present on the page
            # decline_cookies_path = ""
            # cookie_warning = self.driver.find_element(By.XPATH, decline_cookies_path)
            # if cookie_warning:
            #     cookie_warning[0].click()

            username = self.driver.find_element(by=By.NAME, value="username")
            password = self.driver.find_element(by=By.NAME, value="password")

            username.send_keys(USERNAME)
            password.send_keys(PASSWORD)

            time.sleep(random.uniform(1, 3))
            password.send_keys(Keys.ENTER)

            time.sleep(8)

            # close save login
            self.try_click(
                By.XPATH,
                "//div[contains(@role, 'button') and contains(text(), 'Not now')]",
            )

            time.sleep(random.uniform(2, 4))

        except Exception as err:
            log_error(f"Error logging: {err}")

    def like_to_post(self):
        url = ""
        self.driver.get(url)
        time.sleep(4)

        # click here
        try:
            like_button = self.driver.find_element(
                by=By.XPATH, value="//*[@aria-label='Me Gusta']"
            )
            if like_button:
                like_button.click()
                print("Like dado")
        except Exception as err:
            print("no fue posible dar like", err)

    def send_message_to_user(self, url, message):
        self.driver.get(url)
        time.sleep(6)  # O usar esperas explícitas si es dinámico

        try:
            # find first button send message
            click_message = self.try_click(
                By.XPATH,
                "//div[contains(@role, 'button') and contains(text(), 'Message')]",
            )
            time.sleep(random.uniform(1, 3))

            if not click_message:
                # open menu
                self.do_click(By.XPATH, "//header/section[2]/div/div/div[3]")
                time.sleep(random.uniform(1, 3))

                # find button send message
                self.do_click(By.XPATH, "//button[contains(text(), 'Send message')]")
                time.sleep(random.uniform(5, 8))

            # Find the text box for message
            self.do_click(By.XPATH, "//div[@aria-label='Message']")

            message_label = self.driver.find_element(
                by=By.XPATH, value="//div[@aria-label='Message']"
            )
            message_label.send_keys(message)
            time.sleep(random.uniform(1, 3))
            message_label.send_keys(Keys.ENTER)

        except Exception as err:
            log_error(f"an unexpected error occurred: {err}")

    def close_notifications(self):
        if not self.close_notis:
            try:
                close_button = self.driver.find_element(
                    by=By.XPATH,
                    value="//button[contains(@class, '_a9_1') and normalize-space(text())='Not Now']",
                )
                close_button.click()
                self.close_notis = True
            except Exception as err:
                logging.error(f"error {err}")
                print("Not found notification")

    def do_click(self, by, value):
        trying_click = self.try_click(by, value)
        if not trying_click:
            # try close notification
            self.close_notifications()
            time.sleep(2)

        self.try_click(by, value)

    def try_click(self, by, value):
        try:
            element = self.driver.find_element(by=by, value=value)
            element.click()
            return True  # Click successful
        except Exception as err:
            log_error(f"Error clicking element '{value}': {err}")
            return False  # Click failed


bot = InstaFollower()
bot.login()

user_list = user_loop(FILE)

for user_link in user_list:
    bot.send_message_to_user(user_link, MESSAGE)
