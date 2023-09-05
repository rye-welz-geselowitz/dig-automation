from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep 
from flask import Flask, request 
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.chrome.service import Service
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
auth = HTTPBasicAuth()


USERS = {"brl_fellow": generate_password_hash(os.environ.get('PASSWORD'))}

DO_SUBMIT = bool(int(os.environ.get('DO_SUBMIT', 0)))

FORM_URL = "https://airtable.com/appazy8IOBmmwawpc/shrg5Yjk1T6YfJp3u?prefill_Organization=recT7faQO1QBuhJp0&prefill_User%20Role=Member&Status=Requested&hide_User%20Role=true&hide_Status=true&hide_Organization=true"

FIELDS_TO_DIG_LABELS = {
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'mobile': 'Mobile Phone Number',
    'email': 'Email',
    'address': 'Address',
    'referred_by': 'Referred by',
    'sms_opt_in': 'SMS',
    'digital_signature': 'User Agreement Digital Signature'
}

DIG_LABELS_TO_FIELDS = {v:k for k,v in FIELDS_TO_DIG_LABELS.items()}


SMS_OPT_IN_OPTIONS = {'True', 'False'}


def fill_out_form(data):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(FORM_URL)
        form_fields = driver.find_elements(By.CLASS_NAME, "sharedFormField")
        for form_field in form_fields:
            title_element = form_field.find_element(By.CLASS_NAME, 'title')
            key = title_element.text.replace('*', '').strip()
            if key in DIG_LABELS_TO_FIELDS:
                value = data[DIG_LABELS_TO_FIELDS[key]]
                input_element = form_field.find_element(By.TAG_NAME, 'input')
                input_element.send_keys(value)
            elif 'opt out of sms' in key.lower():
                if data['sms_opt_in'] != 'True':
                    cell_container = form_field.find_element(By.CLASS_NAME, 'border-thick') # super brittle lol, find a better way?
                    cell_container.click()

        if DO_SUBMIT:
            submit_button_element = driver.find_element(By.CLASS_NAME, "submitButton") 
            submit_button_element.click()
            message_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "message"))
            )
            assert 'congratulations' in message_element.text.lower()
        else:
            print('Skipping submit!')
    except Exception as e:
        driver.quit()
        raise e
    else:
        driver.quit()
    


@auth.verify_password
def verify_password(username, password):
    if username in USERS and \
            check_password_hash(USERS.get(username), password):
        return username

@app.route("/applications", methods=['POST'])
@auth.login_required
def post_application():
    for field in FIELDS_TO_DIG_LABELS.keys():
        if field not in request.json.keys():
            return {'error': f'Missing field: {field}'}, 400
    sms_opt_in = request.json['sms_opt_in']
    if sms_opt_in not in SMS_OPT_IN_OPTIONS:
        return {'error': f'sms_opt_in must be in: {SMS_OPT_IN_OPTIONS}. Got: {sms_opt_in}'}, 400
    fill_out_form(request.json)
    return {'result': 'success'}, 201
