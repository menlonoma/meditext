from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)

account_sid = "ACa7f75dbd1aa495c95f84c3178c87c96e"
auth_token = "8aec53e337711206ef043bc8c10450ea"
client = TwilioRestClient(account_sid, auth_token)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	number = request.values.get('From')
	msg = request.values.get('Body')
	resp = twilio.twiml.Response()
	resp.message('Hello world')
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
