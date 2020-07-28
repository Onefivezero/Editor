from flask import Flask,flash,request,redirect,send_file,render_template,jsonify

import sqlite3,os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder = "templates")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/upload/', methods = ['GET', 'POST'])
def upfile():
	if request.method == 'POST':
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print("saved file successfully")
			return redirect('/download/'+ filename)
	return render_template('mainsite.html')

@app.route("/download/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

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

if __name__ == "__main__":
    os.mkdir("uploads")
    app.run(host = "0.0.0.0")