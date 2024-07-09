from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import os

def check_appointments(driver):
    today_date = datetime.now().strftime("%d.%m.%Y")
    source_url = "https://tevis.ekom21.de/fra/select2?md=35"
    appointment_check_url = f"https://tevis.ekom21.de/fra/suggest?loc=30&mdt=0&cnc-1039=1&filter_date_from={today_date}&filter_date_to=18.09.2024"
    print(appointment_check_url)
    
    driver.get(source_url)

    # Handle cookie message if it is present
    try:
        wait = WebDriverWait(driver, 10)
        cookie_dismiss_button = wait.until(EC.element_to_be_clickable((By.ID, 'dismiss_button_id')))
        cookie_dismiss_button.click()
        print("Cookie message dismissed")
    except Exception as e:
        print(f"No cookie dialog found or already handled")

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
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'TevisDialog')))
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

    # Extract session cookies from Selenium and convert to requests' format
    selenium_cookies = driver.get_cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

    # Find the first date element and expand it to reveal time slots
    try:
        first_date_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-accordion-header')))
        first_date_element.click()
        print(f"First date element clicked: {first_date_element.text}")
    except Exception as e:
        print(f"Failed to click the first date element: {e}")

    # Extract time slots for the first date and handle the popup after clicking a timeslot
    try:
        time_slots = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'suggest_btn')))
        clickable_time_slot = None
        for time_slot in time_slots:
            if time_slot.is_enabled() and "disabled" not in time_slot.get_attribute("class"):
                clickable_time_slot = time_slot
                break
        
        if clickable_time_slot:
            print(f"First clickable time slot: {clickable_time_slot.get_attribute('title')}")

            # Scroll to the time slot to ensure it is in view
            driver.execute_script("arguments[0].scrollIntoView(true);", clickable_time_slot)
            
            # Click on the first clickable time slot to book it
            actions = ActionChains(driver)
            actions.move_to_element(clickable_time_slot).click().perform()
            print("First clickable time slot clicked")
            
            # Wait for the popup to appear and click 'Ja' button
            try:
                popup_ok_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btn-ok")]'))
                )
                popup_ok_button.click()
                print("'Ja' button in popup clicked")
            except Exception as e:
                print(f"Failed to click the 'Ja' button in the popup: {e}")
        else:
            print("No clickable time slots found")
    except Exception as e:
        print(f"Failed to extract or click time slots: {e}")

    return cookie_dict, appointment_check_url
