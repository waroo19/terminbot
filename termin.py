import requests
from pathlib import Path
import os.path

# get secrets from environment variables

telegram_bot_secret = os.getenv("TELEGRAM_BOT_SECRET")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# urls

session_cookie_source_url = "https://tevis.ekom21.de/fra/select2?md=35"
appointment_check_url = "https://tevis.ekom21.de/fra/location?mdt=217&select_cnc=1&cnc-1039=1"
telegram_send_chat_url = f"https://api.telegram.org/bot{telegram_bot_secret}/sendMessage?chat_id={telegram_chat_id}&text="


def send_telegram_chat(msg):
  response = requests.post(telegram_send_chat_url + str(msg))
  if response.status_code != 200:
    print("Something went wrong with sending telegram messages, are the keys correct?")
    print(response.text)

# if error state file is present, something went wrong so quit the script
if os.path.exists('./error.txt'):
  print("Error state :(")
  quit()

# get session cookie first

session_request = requests.get(session_cookie_source_url)

# send appointment check request with session cookie

check_request = requests.get(appointment_check_url, cookies=session_request.cookies)

if "aktuelle Anliegenauswahl ist leider kein Termin" in check_request.text:
  # send_telegram_chat("Kein Termin verfügbar")
  pass
elif "Es ist ein Fehler aufgetreten" in check_request.text:
  # Error state
  send_telegram_chat("Bot machine broke")
  with open("./error.txt", "w") as f:
    f.write(check_request.text)
else:
  send_telegram_chat("Termin verfügbar")
