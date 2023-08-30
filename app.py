from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep 
from flask import Flask, request 

DO_SUBMIT = True 

FORM_URL = "https://airtable.com/appazy8IOBmmwawpc/shrg5Yjk1T6YfJp3u?prefill_Organization=recT7faQO1QBuhJp0&prefill_User%20Role=Member&Status=Requested&hide_User%20Role=true&hide_Status=true&hide_Organization=true"

FIELDS_TO_DIG_LABELS = {
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'mobile': 'Mobile Phone Number',
    'email': 'Email',
    'address': 'Address',
    'referred_by': 'Referred by',
    'sms_opt_in': 'SMS'
}

DIG_LABELS_TO_FIELDS = {v:k for k,v in FIELDS_TO_DIG_LABELS.items()}


SMS_OPT_IN_OPTIONS = {'True': 'Yes', 'False': 'No'}


def fill_out_form(data):
    driver = webdriver.Chrome()
    driver.get(FORM_URL)
    form_fields = driver.find_elements(By.CLASS_NAME, "sharedFormField")
    for form_field in form_fields:
        title_element = form_field.find_element(By.CLASS_NAME, 'title')
        key = title_element.text.replace('*', '').strip()
        if key in DIG_LABELS_TO_FIELDS:
            value = data[DIG_LABELS_TO_FIELDS[key]]
            input_element = form_field.find_element(By.TAG_NAME, 'input')
            input_element.send_keys(value)
        elif 'sms' in key.lower():
            cell_container = form_field.find_element(By.CLASS_NAME, 'border-thick') # super brittle lol, find a better way?
            cell_container.click()
            options = driver.find_elements(By.CLASS_NAME, "flex-auto") # Also brittle, yikes!
            clicked = False
            target_sms_option = SMS_OPT_IN_OPTIONS[data['sms_opt_in']]
            for option in options:
                if clicked is False:
                    if option.text == target_sms_option:
                        option.click()
                        clicked = True 
            assert clicked, f'Did not find SMS option {target_sms_option}'


    if DO_SUBMIT:
        submit_button_element = driver.find_element(By.CLASS_NAME, "submitButton") 
        submit_button_element.click()
    else:
        print('Skipping submit!')


app = Flask(__name__)


@app.route("/applications", methods=['POST'])
def post_application():
    # TODO: maybe authorize request?
    for field in FIELDS_TO_DIG_LABELS.keys():
        if field not in request.json.keys():
            return {'error': f'Missing field: {field}'}, 400
    sms_opt_in = request.json['sms_opt_in']
    if sms_opt_in not in SMS_OPT_IN_OPTIONS:
        return {'error': f'sms_opt_in must be in: {SMS_OPT_IN_OPTIONS.keys()}. Got: {sms_opt_in}'}, 400
    fill_out_form(request.json)
    return {'result': 'success'}, 201
