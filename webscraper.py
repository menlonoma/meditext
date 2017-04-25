import urllib2
from bs4 import BeautifulSoup

def parse_result(condition):
	result = ""
	words = condition.split()
	for x in words:
		result += x + '+'
	return get_treatment(result)

def get_treatment(diagnosis):
	url = 'https://www.google.com/search?q={0}treatment'.format(diagnosis)
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0')]
	html = opener.open(url).read()
	soup = BeautifulSoup(html, 'html.parser')
	html2 = soup.find_all("div", class_ = "_dyk _wje")
	html1 = soup.find_all("div", class_="_fF _Zni kno-fb-ctx")
	if html1 == []:
		return ' '
	return ' ' + html1[0].text + ' Treatments: ' + html2[0].text + '. '
	#html1 += html2[0]
	#responses = []
	#for x in html1:
		#responses.append(x.text)
	#for x in responses:
		#print x
