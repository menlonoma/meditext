from flask import Flask, request, redirect, session
from twilio import twiml
from twilio.rest import TwilioRestClient
import infermedica_api

# Store cookies for the session and configure Flask app
#

SECRET_KEY = a3knBL401Ajsgk3qr4NB 
app = Flask(__name__)
app.config.from_object(__name__)

# Create a Twilio client with credentials -- may be useful later for
# sending messages without any user input
#

account_sid = "ACa7f75dbd1aa495c95f84c3178c87c96e"
auth_token = "8aec53e337711206ef043bc8c10450ea"
client = TwilioRestClient(account_sid, auth_token)

#configure the api
api = infermedica_api.API(app_id='30d763f7', app_key='91a0b173fc675d415ef8f782a4eff3e8')

# Create diagnosis object with initial patient information.
# Note that time argument is optional here as well as in the add_symptom function



# This gets the question we want to ask, depending on the state that we're in. The session and the 
# q_number are counters stored in the session object, and get reset when we're done with a user
# interaction.
  
def get_question(user_input, state, q_number, a, s, symptoms, prev, conditions):
	#
	# First, we've gotten the initial request and we just ask for symptoms
	#
	if (state == 2):
		session['state'] = 1
		return "Enter your symptoms:"
	#
	# Then, we're in the state where we process the symptoms and return a question
	# 
	elif (state == 1):
		resp = api.parse(user_input)
		profile = infermedica_api.Diagnosis(sex=s, age=a)
		profile.extras['ignore_groups']=True # only single questions
		for item in resp.mentions:
			symptoms.append([item.id, item.choice_id])
			profile.add_symptom(item.id, item.choice_id)
		profile = api.diagnosis(profile)
		session['state'] = 0
		session['symptoms'] = symptoms
		session['prev'] = profile.question.items[0]['id']
		session['conditions'] = profile.conditions
		return profile.question.text
	#
	# Now, we process the yes-no answers to our questions, update the patient
	# object, and stop when our session counter reaches 6.
	#
	else:
		if (q_number < 6):
			if (user_input == 'y'):
				index = 'present'
			elif (user_input == 'n'):
				index = 'absent'
			else: 
				index = 'none' 
			profile = infermedica_api.Diagnosis(sex=s, age=a)
			profile.extras['ignore_groups']=True
			for i in range (len(symptoms)):
				profile.add_symptom(symptoms[i][0], symptoms[i][1])
			profile.add_symptom(prev, index)
			profile = api.diagnosis(profile)
			session['q_number'] = q_number + 1
			symptoms.append([prev, index])
			session['symptoms'] = symptoms
			session['prev'] = profile.question.items[0]['id']
			session['conditions'] = profile.conditions 
			return profile.question.text
	#
	# Once we've asked 6 questions, we reset the session counters and return the
	# most likely diagnosis.
	#
		else:
			session['state'] = 2
			session['q_number'] = 0
			print("Your most likely diagnosis is" + conditions[0]['name'] + " with a %f probability" % conditions[0]['probability'])
			
		

@app.route("/", methods=['GET', 'POST'])
def reply_to_user():

	# Initialize session counters and patient

	state = session.get('state', 2)
	q_number = session.get('q_number', 0)
	age = session.get('age', 35)
	sex = session.get('sex', 'male')
	symptoms = session.get('symptoms', []) 
	prev = session.get('prev')
	conditions = session.get('conditions')
	#patient = session.get('patient', infermedica_api.Diagnosis(sex='male', age=35))
	#patient.extras['ignore_groups']=True # only single questions

	
	# Store properties of the SMS that we received

	number = request.values.get('From')
	msg = request.values.get('Body')

	# Create a response object, call the function above to generate the question, and
	# return it to the user.

        resp = twiml.Response()
	question = get_question(msg, state, q_number, age, sex, symptoms, prev, conditions)
	resp.message(question)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)