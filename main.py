from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time
from dotenv import load_dotenv
import os
import random

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class InstaFollower:
    def __init__(self):
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
        # # Click "Not now" and ignore Save-login info prompt
        # save_login_prompt = self.driver.find_element(
        #     by=By.XPATH, value="//div[contains(text(), 'Not now')]"
        # )
        # if save_login_prompt:
        #     save_login_prompt.click()

        # time.sleep(3)
        # # click "not now" on notifications prompt
        # notifications_prompt = self.driver.find_element(
        #     by=By.XPATH, value="// button[contains(text(), 'Not now')]"
        # )

        # if notifications_prompt:
        #     notifications_prompt.click()

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

    def send_message_to_user(self):
        print("Iniciando envío de mensaje...")
        url = "https://www.instagram.com/ed.briceno/"
        self.driver.get(url)
        time.sleep(6)  # O usar esperas explícitas si es dinámico

        try:
            # Abre el menú
            open_menu = self.driver.find_element(
                by=By.XPATH,
                value="//header/section[2]/div/div/div[3]",
            )
            open_menu.click()
            print("i click here")
            time.sleep(random.uniform(1, 3))

            # Busca el botón de enviar mensaje
            send_message_button = self.driver.find_element(
                by=By.XPATH, value="//button[contains(text(), 'Send message')]"
            )
            send_message_button.click()
            time.sleep(random.uniform(5, 8))

            # Encuentra el cuadro de texto para el mensaje
            message_label = self.driver.find_element(
                by=By.XPATH, value="//div[@aria-label='Message']"
            )
            message_label.click()
            message_label.send_keys("Hola, este es un mensaje automático.")
            time.sleep(random.uniform(1, 3))
            message_label.send_keys(Keys.ENTER)
            print("¡Mensaje enviado exitosamente!")

        except Exception as err:
            print(f"Error al enviar mensaje: {err}")
            # self.driver.save_screenshot("error_screenshot.png")  # Captura para debug


bot = InstaFollower()
bot.login()
bot.send_message_to_user()
