from chrome_driver import get_chromedriver
from telegram_bot import send_telegram_chat
from selenium.webdriver.support.ui import WebDriverWait
from termin import check_appointments
from fill_form import fill_out_form
import os
import requests
from datetime import datetime

def main():
    driver = get_chromedriver(headless=True)
    
    try:
        cookie_dict, appointment_check_url = check_appointments(driver)
         # Wait for the page to load and fill out the form
         #TODO: captcha needs to be solved before filling the form!
        #wait = WebDriverWait(driver, 10)
        #fill_out_form(driver, wait)
    finally:
        driver.quit()

    # Check for error state file
    if os.path.exists('./error.txt'):
        print("Error state :(")
        return

    # Send appointment check request with session cookies
    check_request = requests.get(appointment_check_url, cookies=cookie_dict)

    # Process the response and possibly send Telegram messages
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
        send_telegram_chat("Termin verfügbar")

if __name__ == "__main__":
    main()