from django.shortcuts import render
from django.http import HttpResponse

import requests

import os
import pymongo
from pymongo import MongoClient
import pprint


#the code for connecting with instance of mongodatabase
#needs to be at start of file, as well as the pymongo
#include statements
mongo_url = os.environ.get('MONGODB_URI')
db_name = 'heroku_cnsh2s2r'
client = pymongo.MongoClient(mongo_url)
database = client[db_name]


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    #return render(request, 'index.html')
    r = requests.get('http://httpbin.org/status/418')
    print (r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

#sample for interacting with mongo database, with
#database variable defined above
def db(request):

    text = ''
    post = {"author":"Mike", "text":"post"}
    posts = database['tests']
    posts.insert_one(post)
    for post in posts.find():
        text += post['author']

    return HttpResponse('Hello from Python!' + text)








