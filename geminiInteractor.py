from selenium import webdriver
import pyperclip
import keyboard
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

class GeminiInteractor:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.debugger_address = "127.0.0.1:9222"
        self.driver = webdriver.Chrome(options=options)

    def clear_chat(self):
        try:
            clear_chat_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Clear chat']"))
            )
            clear_chat_button.click()
        except:
            pass

        continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continue']]"))
        )
        continue_button.click()

    def send_message(self, message):
        self.clear_chat()
        textarea = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[@aria-label='User text input']"))
        )
        textarea.click()
        buffer = pyperclip.paste()
        pyperclip.copy(message)
        textarea.send_keys(Keys.CONTROL, 'v')
        run_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Run']"))
        )
        run_button.click()
        pyperclip.copy(buffer)

    def get_all_text(self, element):
        text = element.text
        if "content_copy" in text:
            return ""
        if "Use code with caution" in text:
            return ""
        if len(text) > 0:
            return text
        for child in element.find_elements(By.XPATH, "./*"):
            text += self.get_all_text(child)
        return text

    def is_generating(self):
        spans = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'ng-star-inserted')]"))
        )
        spans2 = []
        for span in spans:
            try:
                if len(span.text) > 0:
                    spans2.append(self.get_all_text(span))
            except:
                pass
        return 'Stop' in spans2

    def get_last_message(self):

        spans = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'prompt-container')]"))
        )
        spans2 = []
        for span in spans:
            if len(span.text) > 0:
                spans2.append(span.text)
        return spans2[-1]
