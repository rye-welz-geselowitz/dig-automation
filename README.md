Deployed @ https://dig-automation-35828ef88d43.herokuapp.com

# Usage 
The purpose of this service is to help fellows automate moving data from TypeForm to the DIG app. 

To take advantage of this service, **simply make a copy of [this](https://zapier.com/shared/e3d3b9242c1d94f7785704c75d613eed24713d21) Zap and customize it to your purposes.**

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
curl -X POST http://127.0.0.1:5000/applications  -H "Content-Type: application/json" --data-raw '{"first_name": "Test", "last_name": "McTest", "mobile": "+15555555555", "email": "test@example.com", "address": "11225", "referred_by": "WIC", "sms_opt_in": "True"}' -u "brl_fellow:some_password"
``````

``````
curl -X POST https://2e4b-71-247-2-201.ngrok-free.app/applications  -H "Content-Type: application/json" --data-raw '{"first_name": "Test", "last_name": "McTest", "mobile": "+15555555555", "email": "test@example.com", "address": "11225", "referred_by": "WIC", "sms_opt_in": "True"}' -u "brl_fellow:some_password"
``````


https://2e4b-71-247-2-201.ngrok-free.app