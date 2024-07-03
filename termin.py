import requests
from pathlib import Path
import os.path

# get secrets from environment variables

telegram_bot_secret = os.getenv("TELEGRAM_BOT_SECRET")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# urls

session_cookie_source_url = "https://tevis.ekom21.de/stdar/select2?md=4"
appointment_check_url = "https://tevis.ekom21.de/stdar/suggest?mdt=78&select_cnc=1&cnc-1653=0&cnc-1651=0&cnc-1655=1&cnc-1721=0&cnc-1720=0&cnc-1663=0&cnc-1656=0&cnc-1658=0&cnc-1659=0&cnc-1654=0&cnc-1660=0&cnc-1661=0&cnc-1674=0&cnc-1675=0&cnc-1665=0&cnc-1667=0&cnc-1668=0&cnc-1669=0&cnc-1670=0&cnc-1672=0&cnc-1673=0&cnc-1652=0&cnc-1662=0&cnc-1657=0&cnc-1664=0&cnc-1671=0&cnc-1666=0&cnc-1676=0"
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
