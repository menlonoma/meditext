from flask import Flask, request, redirect
from twilio import twiml
from twilio.rest import TwilioRestClient

application = Flask(__name__)

account_sid = "ACa7f75dbd1aa495c95f84c3178c87c96e"
auth_token = "8aec53e337711206ef043bc8c10450ea"
client = TwilioRestClient(account_sid, auth_token)

@application.route("/", methods=['GET', 'POST'])
def hello_monkey():
	number = request.values.get('From')
	msg = request.values.get('Body')
	resp = twiml.Response()
	resp.message('Hello world')
	return str(resp)

if __name__ == "__main__":
	application.run(debug=True)
