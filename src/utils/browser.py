from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from src.constants.config import WAIT_TIME, HEADLESS, COOKIE_SELECTORS

def init_browser():
    """Initialize and return a configured Firefox browser instance."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless")
    
    service = Service(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=service, options=options)
    browser.implicitly_wait(WAIT_TIME)
    return browser


def handle_cookie_consent(browser):
    """Handle cookie consent popups using common selectors."""
    for selector in COOKIE_SELECTORS:
        try:
            button = WebDriverWait(browser, WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            try:
                button.click()
                return True
            except:
                # Fallback to JavaScript click if standard click fails
                browser.execute_script("arguments[0].click();", button)
                return True
        except:
            continue
    return False 