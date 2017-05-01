import webscraper


counter = 0
correct = 0

file = open("test.txt", "r") 
for line in file: 
	counter = counter + 1
	treatment = webscraper.parse_result(line)
	if (treatment != ' '):
		correct = correct + 1

print ("num correct") 
print (correct)
print ("total")
print (counter)

#diseases.txt (infermedica) - 294 of 566
#wikidiseases.txt (wikipedia list of infectious diseases) 83 of 232
#cdc.txt (cdc most popular topics) 22 of 35
#ri.txt (rhode island dept of health) 48 of 107