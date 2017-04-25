from flask import Flask, request, redirect, session
from twilio import twiml
from twilio.rest import TwilioRestClient
import infermedica_api
import webscraper

#
# Store cookies for the session and configure Flask app
#

SECRET_KEY = 'a3knBL401Ajsgk3qr4NB' 
application = Flask(__name__)
application.config.from_object(__name__)

#
# Create a Twilio client with credentials -- may be useful later for
# sending messages without any user input
#

account_sid = "ACa7f75dbd1aa495c95f84c3178c87c96e"
auth_token = "8aec53e337711206ef043bc8c10450ea"
client = TwilioRestClient(account_sid, auth_token)

#configure the api
api = infermedica_api.API(app_id='30d763f7', app_key='91a0b173fc675d415ef8f782a4eff3e8')

# This function gets the question we want to ask, depending on the state that we're in. The state and the 
# q_number are counters stored in the session object, and get reset when we're done with a user
# interaction. Every time the function is called, it's passed in the current patient information.
  
def get_question(user_input, state, q_number, a, s, symptoms, prev, conditions):
	#
	# If the user wants to restart, they can enter Q and quit.
	#
	user_input = user_input.lower()
	if (user_input == 'q' or user_input == 'Q'):
		session['state'] = 4
		session['q_number'] = 0
		return "Thanks"
	#
	# If after 10 questions, the user just wants more info on their diagnosis as
 	# they continue, they can request it.
	#
	elif (user_input == 'more info'):
		length = len(conditions)
		probability0 = conditions[0]['probability'] * 100
		info0 = api.condition_details(conditions[0]['id'])
		severity0 = get_severity(info0.severity)
		treatment = webscraper.parse_result(conditions[0]['name'])
		text = "Your most likely diagnosis is " + conditions[0]['name'] + " with a %.0f%% probability. " % probability0 + severity0 + info0.extras['hint'] + '\n' + treatment + '\n'
		if (length >= 2):
			probability1 = conditions[1]['probability'] * 100
			info1 = api.condition_details(conditions[1]['id'])
			severity1 = get_severity(info1.severity)
			text += " Your second most likely diagnosis is " + conditions[1]['name'] + " with a %.0f%% probability. " % probability1 + severity1 + info1.extras['hint'] + '\n'	
		if (length > 2):
			probability2 = conditions[2]['probability'] * 100
			info2 = api.condition_details(conditions[2]['id'])
			severity2 = get_severity(info2.severity)
			text += " Your third most likely diagnosis is " + conditions[2]['name'] + " with a %.0f%% probability. " % probability2 + severity2 + info2.extras['hint']
		
		
		
		return text

	#
	# In states 4-2, we just start the user interaction, asking for age, sex, and symptoms. 
	elif (state == 4):
		session ['state'] = 3
		return "Welcome to meditext. Text 'q' at any time to quit. Please enter your age: "
	elif (state == 3):
		try:
			session ['age'] = int(user_input)
			session ['state'] = 2
			return "Enter your sex (M/F): "
		except ValueError: 
			return "Enter your age (as a number): "
	elif (state == 2):
		session ['state'] = 1
		user_input = user_input.lower()
		if (user_input[0] == 'm'):
			session ['sex'] = 'male'
		else: 
			session ['sex'] = 'female'
		return "Enter your symptoms:"
	#
	# Then, we're in the state where we process the symptoms and return a question.
	# If we cannot parse any symptoms from user input, we will tell them to be more
	# specific. Otherwise, we return a question and move to state 0.
	# 
	elif (state == 1):
		resp = api.parse(user_input)
		profile = infermedica_api.Diagnosis(sex=s, age=a)
		profile.extras['ignore_groups']=True # only single questions
		for item in resp.mentions:
			symptoms.append([item.id, item.choice_id])
			profile.add_symptom(item.id, item.choice_id)
		if (len(symptoms) == 0):
			return "No symptoms found. Please be more specific"
		profile = api.diagnosis(profile)
		session['state'] = 0
		session['symptoms'] = symptoms
		session['prev'] = profile.question.items[0]['id']
		session['conditions'] = profile.conditions
		return profile.question.text
	#
	# Now, we process the yes-no answers to our questions. If we don't have a 
	# diagnosis with 90% probability, we keep asking questions.
	#
	else:
		if (conditions[0]['probability'] < .9):
			user_input = user_input.lower()
			if (user_input == 'y' or user_input == 'yes'):
				index = 'present'
			elif (user_input == 'n' or user_input == 'no'):
				index = 'absent'
			else: 
				index = 'unknown' 
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
			#
			# If we've asked 10 questions, then we return their 3 
			# most likely diagnoses with each subsequent question.
			# The user can then request more info.
			#
			if (q_number <= 10):
				return profile.question.text
			else:
				probability = conditions[0]['probability'] * 100
				return ("Your three most likely diagnoses are " + conditions[0]['name'] + ", " + conditions[1]['name'] + ", " + conditions[2]['name'] + ". For more information, text 'more info'.  To continue, answer the following question: " + profile.question.text)
	#
	# Once we've gotten to 90% probability, we return a diagnosis with treatment
	# details. 
	#
		else:
			session['state'] = 4
			session['q_number'] = 0			
			length = len(conditions)
			probability0 = conditions[0]['probability'] * 100
			info0 = api.condition_details(conditions[0]['id'])
			severity0 = get_severity(info0.severity)
			treatment = webscraper.parse_result(conditions[0]['name'])
			text = "Your most likely diagnosis is " + conditions[0]['name'] + " with a %.0f%% probability. " % probability0 + severity0 + info0.extras['hint'] + '\n' + treatment + '\n'
			if (length >= 2):
				probability1 = conditions[1]['probability'] * 100
				info1 = api.condition_details(conditions[1]['id'])
				severity1 = get_severity(info1.severity)
				text += " Your second most likely diagnosis is " + conditions[1]['name'] + " with a %.0f%% probability. " % probability1 + severity1 + info1.extras['hint'] + '\n'	
			if (length > 2):
				probability2 = conditions[2]['probability'] * 100
				info2 = api.condition_details(conditions[2]['id'])
				severity2 = get_severity(info2.severity)
				text += " Your third most likely diagnosis is " + conditions[2]['name'] + " with a %.0f%% probability. " % probability2 + severity2 + info2.extras['hint']			
		
			return text

def get_severity(severity):
	if (severity == 'mild'):
		return 'See a doctor if symptoms worsen. '
	elif (severity == 'moderate'):
		return 'See a doctor soon. '
	else:
		return 'See a doctor immediately. '
	

@application.route("/", methods=['GET', 'POST'])
def reply_to_user():

	# Initialize session counters and patient information.
	# This information will be passed to get_question every time we get a reply.

	state = session.get('state', 4)
	q_number = session.get('q_number', 0)
	age = session.get('age')
	sex = session.get('sex')
	symptoms = session.get('symptoms', []) 
	prev = session.get('prev')
	conditions = session.get('conditions')

	# Store properties of the SMS that we received

	number = request.values.get('From')
	msg = request.values.get('Body')

	# Create a response object, call get_question to generate the question, and
	# return it to the user.

        resp = twiml.Response()
	question = get_question(msg, state, q_number, age, sex, symptoms, prev, conditions)
	resp.message(question)
	return str(resp)

if __name__ == "__main__":
	application.run(debug=True)
