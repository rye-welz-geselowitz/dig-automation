Deployed @ https://dig-automation-35828ef88d43.herokuapp.com

# Usage 
The purpose of this service is to help fellows automate moving data from TypeForm to the DIG app. 

To take advantage of this service, create a [Zap](https://zapier.com/) that triggers whenever a new row is added to your TypeForm:

<img src="https://github.com/rye-welz-geselowitz/dig-automation/blob/main/screenshots/step_1.png?raw=true" width="200">

For the main "action," use "Code by Zapier" ("Run Python Code). (NOTE: You can alternatively also use Webhook by Zapier if you have a premium Zapier account.) Map the fields from your TypeForm as follows:
<img src="https://github.com/rye-welz-geselowitz/dig-automation/blob/main/screenshots/step_2.png?raw=true" width="300">

Then paste in this code snippet:
```
import requests 
from requests.auth import HTTPBasicAuth

PASSWORD = '<PASSWORD>'

basic_auth = HTTPBasicAuth('brl_fellow', PASSWORD)

URL = 'https://dig-automation-35828ef88d43.herokuapp.com/applications'
response = requests.post(URL, json=input_data, auth=basic_auth)

try:
    result = response.json()
except Exception as e:
    result = {}

output = [{'result': str(result)}]

```
(Be sure to replace `<PASSWORD>` with an actual password - ask Rye!)


Finally, set up an SMS notification to alert you of the automation result. This way you'll know if anything goes wrong!

<img src="https://github.com/rye-welz-geselowitz/dig-automation/blob/main/screenshots/step_3.png?raw=true" width="300">


# Running locally
### Create virtualenv
python3 -m venv automation-venv

### Activate virtualenv
source automation-venv/bin/activate

### Install requirements
pip install -r requirements.txt 

### Run flask app  
PASSWORD=some_password flask run

### (For testing against Zapier): Run ngrok
ngrok http http://127.0.0.1:5000

### Running gunicorn
gunicorn app:app

### Sample curl requests:

``````
curl -X POST http://127.0.0.1:5000/applications  -H "Content-Type: application/json" --data-raw '{"first_name": "Test", "last_name": "McTest", "mobile": "+15555555555", "email": "test@example.com", "address": "11225", "referred_by": "WIC", "sms_opt_in": "True", "digital_signature": "Test Person"}' -u "brl_fellow:some_password"
``````

