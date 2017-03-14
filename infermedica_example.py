import infermedica_api

#configure the api
api = infermedica_api.API(app_id='30d763f7', app_key='91a0b173fc675d415ef8f782a4eff3e8')

# Create diagnosis object with initial patient information.
# Note that time argument is optional here as well as in the add_symptom function
request = infermedica_api.Diagnosis(sex='male', age=35)

request.extras['ignore_groups']=True # only single questions

#symptom parsing from user text
text = input("Enter your symptoms: ")
response = api.parse(text)

for item in response.mentions:
	print(item.name)
	print(item.id)
	request.add_symptom(item.id, item.choice_id)
#print(response, end="\n\n")

#print(request, end="\n\n")

#request.add_symptom('s_21', 'present')
#request.add_symptom('s_98', 'present')
#request.add_symptom('s_107', 'absent')

#request.set_pursued_conditions(['c_33', 'c_49'])  # Optional

# call diagnosis

request = api.diagnosis(request)

#print(request.extras, end= "\n\n")
for i in range(1,6):

	# Access question asked by API
	#print(request.question)
	#print("here ")
	#print(request.question.type)
	#print(request.question.text)  # actual text of the question
	#print(request.question.items)  # list of related evidences with possible answers
	#print(request.question.items[0]['id'])
	#print(request.question.items[0]['name'])
	#print(request.question.items[0]['choices'])  # list of possible answers
	#print(request.question.items[0]['choices'][0]['id'])  # answer id
	#print(request.question.items[0]['choices'][0]['label'])  # answer label
	ans = input(request.question.text + ' ')

	if (ans == 'y'):
		index = 0
	elif (ans == 'n'):
		index = 1
	else:
		index = 2
	# Access list of conditions with probabilities
	#print(request.conditions)
	#print(request.conditions[0]['id'])
	#print(request.conditions[0]['name'])
	#print(request.conditions[0]['probability'])

	# Next update the request and get next question:
	request.extras['ignore_groups']=True
	request.add_symptom(request.question.items[0]['id'], request.question.items[0]['choices'][index]['id'])
	#print("hi")
	# call diagnosis method again
	request = api.diagnosis(request)
print("You're most likely diagnosis is " + request.conditions[0]['name'] + " with a %f probability" % request.conditions[0]['probability'])












