import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

today_date = datetime.now().strftime("%d.%m.%Y")

# Set up headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# Get secrets from environment variables
telegram_bot_secret = os.getenv("TELEGRAM_BOT_SECRET")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# URLs
session_cookie_source_url = "https://tevis.ekom21.de/fra/select2?md=35"
appointment_check_url = f"https://tevis.ekom21.de/fra/suggest?loc=30&mdt=0&cnc-1039=1&filter_date_from={today_date}&filter_date_to=30.10.2024"
print(appointment_check_url)
telegram_send_chat_url = f"https://api.telegram.org/bot{telegram_bot_secret}/sendMessage?chat_id={telegram_chat_id}&text="

def send_telegram_chat(msg):
    response = requests.post(telegram_send_chat_url + str(msg))
    if response.status_code != 200:
        print("Something went wrong with sending telegram messages, are the keys correct?")
        print(response.text)

driver.get(session_cookie_source_url)

# Handle cookie message
try:
    wait = WebDriverWait(driver, 5)
    cookie_dismiss_button = wait.until(EC.element_to_be_clickable((By.ID, 'dismiss_button_id')))
    cookie_dismiss_button.click()
except Exception as e:
    print(f"No cookie dialog found or already handled: {e}")

# Scroll to and click the '+' button
try:
    plus_button = wait.until(EC.element_to_be_clickable((By.ID, 'button-plus-1039')))
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()
except Exception as e:
    print(f"Failed to click the '+' button: {e}")

# Click the 'Weiter' button
try:
    weiter_button = wait.until(EC.element_to_be_clickable((By.ID, 'WeiterButton')))
    weiter_button.click()
except Exception as e:
    print(f"Failed to click the 'Weiter' button: {e}")

try:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'TevisDialog')))
    ok_button = driver.find_element(By.ID, 'OKButton')
    ok_button.click()
    print("'OK' button clicked")
except Exception as e:
    print(f"Modal handling error: {e}")

# Click the final button
try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "select_location"))
    )
    driver.execute_script("arguments[0].click();", button)
    print("Button clicked using JavaScript")
except Exception as e:
    print("Failed to click the button using JavaScript:", e)

# Extract session cookies from Selenium and convert to requests format
selenium_cookies = driver.get_cookies()
cookie_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
driver.quit()

# Check for error state
if os.path.exists('./error.txt'):
    print("Error state :(")
    quit()

# Send appointment check request with session cookies
check_request = requests.get(appointment_check_url, cookies=cookie_dict)

# Process response
if "Keine Zeiten verfügbar" in check_request.text:
    log_message = "Kein Termin verfügbar"
    print(log_message)
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {log_message}\n")
elif "Es ist ein Fehler aufgetreten" in check_request.text:
    send_telegram_chat("Bot machine broke")
    with open("./error.txt", "w", encoding='utf-8') as f:
        f.write(check_request.text)
else:
    send_telegram_chat("Termin verfügbar!")
