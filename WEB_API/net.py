from flask import Flask
from flask import request, jsonify
import sqlite3

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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
		
@app.route('/printbook')
def print_book():
	query_parameters = request.args
	author = query_parameters.get("author")
	year = query_parameters.get("year")
	rating = query_parameters.get("rating")
	
	to_print = []
	if author:
		to_print.append(author)
	if year:	
		to_print.append(year)
	if rating:
		to_print.append(rating)
	if not(author or year or rating):
		return "ERROR"
	return jsonify(to_print)
	
@app.route('/book')
def db_read():
	#url'de verilen parametreleri query_parameters degiskenine ata
	query_parameters = request.args
	
	#url parametrelerini python'daki parametrelere atama
	id = query_parameters.get('id')
	published = query_parameters.get('published')
	author = query_parameters.get('author')

	#query ve filter tanimlama
	query = "SELECT * FROM books WHERE"
	to_filter = []

	#query ve filtera ekleme
	if id:
		query += ' id=? AND'
		to_filter.append(id)
	if published:
		query += ' published=? AND'
		to_filter.append(published)
	if author:
		query += ' author=? AND'
		to_filter.append(author)
	if not (id or published or author):
		return "Error 404 nothing found"
		
	#query'nin sonundaki "AND" kismini silme
	query = query[:-4] + ';'
	
	#veritabani baglantisi
	conn = sqlite3.connect('books.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()

	#sonucu results arrayine(tuple?) atama
	results = cur.execute(query, to_filter).fetchall()

	#results ciktisi al
	return jsonify(results)
