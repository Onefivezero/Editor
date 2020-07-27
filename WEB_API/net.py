from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def intro():
	return "Merhaba Dünya"
	
@app.route('/print/<some_string>')
def printer(some_string):
	return "Print: %s" % some_string
	
@app.route('/printx')
def printvar():
	query_parameters = request.args
	id = query_parameters.get("id")
	if id:
		return id
	else:
		return "Nothing"