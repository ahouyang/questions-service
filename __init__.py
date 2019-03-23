from flask import Flask, request, render_template, make_response, jsonify
from flask_restful import Resource, Api, reqparse
import pymongo
import datetime
import sys
import smtplib, ssl
import string
import random
import time

app = Flask(__name__)
api = Api(app)

class AddQuestion(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('title')
		parser.add_argument('body')
		parser.add_argument('username')
		parser.add_argument('tags', action='append')
		args = parser.parse_args()
		questions = get_questions_coll()
		idnum = questions.count() + 1
		question = {}
		question['id'] = args['username'] + '_q_' + str(idnum) 
		question['title'] = args['title']
		question['body'] = args['body']
		question['username'] = args['username']
		question['tags'] = args['tags']
		question['score'] = 0
		question['view_count'] = 0
		question['answer_count'] = 0
		question['timestamp'] = time.time()
		question['accepted_answer_id'] = None
		question['media'] = []
		questions.insert_one(question)
		return {'status': 'OK', 'id': question['id']}

def parse_args_list(argnames):
	parser = reqparse.RequestParser()
	for arg in argnames:
		parser.add_argument(arg)
	args = parser.parse_args()
	return args

def get_questions_coll():
	myclient = pymongo.MongoClient('mongodb://130.245.170.88:27017/')
	mydb = myclient['finalproject']
	users = mydb['questions']
	return users

api.add_resource(AddQuestion, '/add')



if __name__ == '__main__':
	app.run(debug=True)