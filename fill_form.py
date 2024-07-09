from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from data import personal_info

def fill_out_form(driver, wait):
    try:

        wait.until(EC.presence_of_element_located((By.ID, 'sexselect-button'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, f'//li[@data-val="{personal_info["sex"]}"]'))).click()

        driver.find_element(By.ID, 'vorname').send_keys(personal_info['vorname'])
        driver.find_element(By.ID, 'nachname').send_keys(personal_info['nachname'])
        driver.find_element(By.ID, 'email').send_keys(personal_info['email'])
        driver.find_element(By.ID, 'emailwhlg').send_keys(personal_info['emailCheck'])
        driver.find_element(By.ID, 'geburtsdatumDay').send_keys(personal_info['geburtsdatumDay'])
        driver.find_element(By.ID, 'geburtsdatumMonth').send_keys(personal_info['geburtsdatumMonth'])
        driver.find_element(By.ID, 'geburtsdatumYear').send_keys(personal_info['geburtsdatumYear'])
        driver.find_element(By.ID, 'str').send_keys(personal_info['anschrift'])
        driver.find_element(By.ID, 'plz').send_keys(personal_info['postleitzahl'])
        driver.find_element(By.ID, 'wohnort').send_keys(personal_info['wohnort'])
        driver.find_element(By.ID, 'captcha_result').send_keys(personal_info['captcha_code']) # captcha techniques?

        # Agree to the privacy policy
        driver.find_element(By.NAME, 'agreementChecked').click()

        # Submit the form
        submit_button = driver.find_element(By.ID, 'chooseTerminButton')
        driver.execute_script("arguments[0].click();", submit_button)

        print("Form filled out and submitted successfully.")
    except Exception as e:
        print(f"Failed to fill out the form: {e}")
