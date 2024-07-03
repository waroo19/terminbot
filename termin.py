import requests
import os
from datetime import datetime, timedelta

# Get secrets from environment variables
telegram_bot_secret = os.getenv("TELEGRAM_BOT_SECRET")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# URLs
session_cookie_source_url = "https://tevis.ekom21.de/fra/select2?md=35"
appointment_check_url = "https://tevis.ekom21.de/fra/location?mdt=217&select_cnc=1&cnc-1039=1"
telegram_send_chat_url = f"https://api.telegram.org/bot{telegram_bot_secret}/sendMessage?chat_id={telegram_chat_id}&text="

def send_telegram_chat(msg):
    response = requests.post(telegram_send_chat_url + str(msg))
    if response.status_code != 200:
        print("Something went wrong with sending telegram messages, are the keys correct?")
        print(response.text)

# If error state file is present, something went wrong so quit the script
if os.path.exists('./error.txt'):
    print("Error state :(")
    quit()

# Get session cookie first
session_request = requests.get(session_cookie_source_url)
if session_request.status_code != 200:
    print("Failed to get session cookie")
    print(session_request.text)
    quit()

# Debugging: Print session request response
print("Session request response text:")
print(session_request.text)

# Send appointment check request with session cookie
check_request = requests.get(appointment_check_url, cookies=session_request.cookies)
if check_request.status_code != 200:
    print("Failed to check appointments")
    print(check_request.text)
    quit()

# Debugging: Print appointment check response
print("Appointment check response text:")
print(check_request.text)

try:
    appointments = check_request.json()
    print("Parsed JSON response:")
    print(appointments)  # Print the parsed JSON response for debugging
except ValueError:
    print("Failed to parse JSON response")
    print(check_request.text)
    quit()

# Define the date range
today = datetime.today()
two_weeks_from_now = today + timedelta(days=14)

# Check the response text for error messages
if "aktuelle Anliegenauswahl ist leider kein Termin" in check_request.text:
    print("Kein Termin verfügbar")
elif "Es ist ein Fehler aufgetreten" in check_request.text:
    # Error state
    send_telegram_chat("Bot machine broke")
    with open("./error.txt", "w") as f:
        f.write(check_request.text)
else:
    # Check for available appointments within the next two weeks
    available = False
    # Improved debugging: Print structure of JSON data
    if 'data' in appointments:
        for appointment in appointments['data']:
            print("Appointment entry:", appointment)  # Print each appointment entry
            if 'date' in appointment:
                try:
                    appointment_date = datetime.strptime(appointment['date'], '%Y-%m-%d')
                    if today <= appointment_date <= two_weeks_from_now:
                        available = True
                        break
                except ValueError as e:
                    print(f"Date parsing error: {e}")
            else:
                print("No date in appointment entry")
    else:
        print("No 'data' key in JSON response")

    if available:
        send_telegram_chat("Termin verfügbar in den nächsten 2 Wochen")
    else:
        send_telegram_chat("Kein Termin verfügbar in den nächsten 2 Wochen")
