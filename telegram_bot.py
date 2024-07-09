import os
import requests

def send_telegram_chat(msg):
    telegram_bot_secret = os.getenv("TELEGRAM_BOT_SECRET")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Ensure the secrets are fetched correctly
    if not telegram_bot_secret or not telegram_chat_id:
        raise ValueError("Telegram bot secret or chat ID not set in environment variables")
    
    telegram_send_chat_url = f"https://api.telegram.org/bot{telegram_bot_secret}/sendMessage?chat_id={telegram_chat_id}&text="
    response = requests.post(telegram_send_chat_url + str(msg))
    if response.status_code != 200:
        print("Something went wrong with sending telegram messages, are the keys correct?")
        print(response.text)
