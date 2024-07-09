from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_chromedriver(headless=True):
    options = Options()
    if headless:
        options.headless = True  # Run in headless mode if needed

    # Use webdriver-manager to manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver