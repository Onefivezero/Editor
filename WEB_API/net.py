from flask import Flask

app = Flask(__name__)

@app.route('/')
def intro():
	return "Merhaba Dünya"
	
@app.route('/print/<some_string>')
def printer(some_string):
	return "Print: %s" % some_string