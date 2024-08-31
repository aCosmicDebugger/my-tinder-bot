import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
from dotenv import load_dotenv

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega as variáveis do .env
load_dotenv()

username = os.getenv("TINDER_USERNAME")
password = os.getenv("TINDER_PASSWORD")
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
brave_path = os.getenv("BRAVE_BROWSER_PATH")

class TinderBot:
    def __init__(self):
        logging.info("Inicializando o navegador...")

        chrome_options = Options()
        chrome_options.binary_location = brave_path
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")

        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Navegador iniciado.")

        # Carregar cookies
        self.load_cookies()

    def load_cookies(self):
        logging.info("Carregando cookies...")
        try:
            self.driver.get('https://tinder.com')
            with open('cookies.json', 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    # Adaptação para a estrutura do cookie
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
            logging.info("Cookies carregados.")
        except Exception as e:
            logging.error(f"Erro ao carregar cookies: {e}")

    def login(self):
        try:
            # Verifica se já está logado
            self.driver.get('https://tinder.com')
            if "dashboard" in self.driver.current_url:
                logging.info("Já está logado.")
                return

            logging.info("Acessando o site do Tinder...")
            self.driver.get('https://tinder.com/pt')

            logging.info("Clicando no botão 'Entrar'...")
            entrar_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//div[text()="Entrar"]'))
            )
            entrar_btn.click()

            logging.info("Esperando o botão 'Entrar com o Google'...")
            entrar_com_google_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Continuar com o Google"]'))
            )
            logging.info("Clicando no botão 'Continuar com o Google'...")
            entrar_com_google_btn.click()

            logging.info("Esperando a nova janela do pop-up abrir...")
            WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))
            original_window = self.driver.current_window_handle
            all_windows = self.driver.window_handles
            for window in all_windows:
                if window != original_window:
                    self.driver.switch_to.window(window)
                    break

            logging.info("Esperando o campo de email...")
            email_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="identifierId" and @type="email"]'))
            )
            logging.info("Preenchendo o email...")
            email_input.send_keys(username)

            logging.info("Esperando o botão 'Próxima' para email...")
            self.click_next_button()

            logging.info("Esperando o campo de senha...")
            password_input = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="password" and @type="password"]'))
            )
            logging.info("Preenchendo a senha...")
            password_input.send_keys(password)

            logging.info("Esperando o botão 'Próxima' para senha...")
            self.click_next_button()

            self.driver.switch_to.window(original_window)

            logging.info("Esperando o login completar...")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="mainContent"]'))
            )
            logging.info("Login completado.")

        except Exception as e:
            logging.error(f"Erro durante o login: {e}")
            self.driver.quit()

    def click_next_button(self):
        try:
            next_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Próxima") or contains(text(), "Next")]'))
            )
            logging.info("Clicando no botão 'Próxima' ou 'Next'...")
            next_btn.click()
        except Exception as e:
            logging.error(f"Erro ao clicar no botão 'Próxima': {e}")

    def like(self):
        try:
            logging.info("Clicando no botão 'Like'...")
            like_btn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]')
            like_btn.click()
        except Exception as e:
            logging.error(f"Erro ao clicar no botão 'Like': {e}")

    def dislike(self):
        try:
            logging.info("Clicando no botão 'Dislike'...")
            dislike_btn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
            dislike_btn.click()
        except Exception as e:
            logging.error(f"Erro ao clicar no botão 'Dislike': {e}")

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def close_popup(self):
        try:
            logging.info("Fechando popup...")
            popup_3 = self.driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div[2]/button[2]')
            popup_3.click()
        except Exception as e:
            logging.error(f"Erro ao fechar popup: {e}")

    def close_match(self):
        try:
            logging.info("Fechando popup de match...")
            match_popup = self.driver.find_element(By.XPATH, '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
            match_popup.click()
        except Exception as e:
            logging.error(f"Erro ao fechar popup de match: {e}")

bot = TinderBot()
bot.login()
