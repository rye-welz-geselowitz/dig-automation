
Deployed @ https://dig-automation-35828ef88d43.herokuapp.com/applications

# Running locally
### Create virtualenv
python3 -m venv automation-venv

### Activate virtualenv
source automation-venv/bin/activate

### Install requirements
pip install -r requirements.txt 

### Run flask app 
flask run

### (For testing against Zapier): Run ngrok
ngrok http http://127.0.0.1:5000

### Running gunicorn
gunicorn app:app

### Sample curl requests:

````
curl -X POST http://127.0.0.1:5000/applications  -H "Content-Type: application/json" --data-raw '{"first_name": "Test"}'
curl -X POST https://7db4-71-247-2-201.ngrok-free.app/applications  -H "Content-Type: application/json" --data-raw '{"name": "testuser"}'
````


