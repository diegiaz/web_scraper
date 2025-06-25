import os
from dotenv import load_dotenv

load_dotenv("config.env")

# URLs
MAIN_URL = "https://apps.feriavalencia.com/catalog/cevisama/exhibitors"
LOGIN_URL = "https://example.com/login"  # optional

# Output configuration
OUTPUT_CSV = "output.csv"
OUTPUT_DIR = "src/outputs"

# Test configuration
TEST_MODE = True
TEST_LIMIT = 5

# Browser configuration
WAIT_TIME = 5
HEADLESS = False

# Authentication (optional, now loaded from env)
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Cookie consent selectors
COOKIE_SELECTORS = [
    "//button[contains(text(), 'Aceptar')]",
    "//button[contains(text(), 'Accept')]",
    "//button[contains(text(), 'De acuerdo')]",
    "//a[contains(text(), 'Aceptar')]",
    "//a[contains(text(), 'De acuerdo')]",
    "//button[contains(@class, 'cookie')]",
    "//div[contains(@class, 'cookie')]//button",
    "//div[contains(@id, 'cookie')]//button",
    "//button[contains(@id, 'accept')]",
    "//button[contains(@id, 'agree')]",
] 