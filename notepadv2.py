from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from pytodb_v2 import *
import os
import sys
import requests

#SYNTAX HIGHLIGHT BASLANGIC
def format(color, style=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QColor()
	_color.setNamedColor(color)

	_format = QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)

	return _format


# Syntax styles that can be shared by all languages
STYLES = {
	'keyword': format('blue'),
	'operator': format('red'),
	'brace': format('darkGray'),
	'defclass': format('black', 'bold'),
	'string': format('magenta'),
	'string2': format('darkMagenta'),
	'comment': format('darkGreen', 'italic'),
	'self': format('black', 'italic'),
	'numbers': format('brown'),
}


class PythonHighlighter (QSyntaxHighlighter):
	"""Syntax highlighter for the Python language.
	"""
	# Python keywords
	keywords = [
		'and', 'assert', 'break', 'class', 'continue', 'def',
		'del', 'elif', 'else', 'except', 'exec', 'finally',
		'for', 'from', 'global', 'if', 'import', 'in',
		'is', 'lambda', 'not', 'or', 'pass', 'print',
		'raise', 'return', 'try', 'while', 'yield',
		'None', 'True', 'False',
	]

	# Python operators
	operators = [
		'=',
		# Comparison
		'==', '!=', '<', '<=', '>', '>=',
		# Arithmetic
		'\+', '-', '\*', '/', '//', '\%', '\*\*',
		# In-place
		'\+=', '-=', '\*=', '/=', '\%=',
		# Bitwise
		'\^', '\|', '\&', '\~', '>>', '<<',
	]

	# Python braces
	braces = [
		'\{', '\}', '\(', '\)', '\[', '\]',
	]
	def __init__(self, document):
		QSyntaxHighlighter.__init__(self, document)

		# Multi-line strings (expression, flag, style)
		# FIXME: The triple-quotes in these two lines will mess up the
		# syntax highlighting from this point onward
		self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
		self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

		rules = []

		# Keyword, operator, and brace rules
		rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
			for w in PythonHighlighter.keywords]
		rules += [(r'%s' % o, 0, STYLES['operator'])
			for o in PythonHighlighter.operators]
		rules += [(r'%s' % b, 0, STYLES['brace'])
			for b in PythonHighlighter.braces]

		# All other rules
		rules += [
			# 'self'
			(r'\bself\b', 0, STYLES['self']),

			# Double-quoted string, possibly containing escape sequences
			(r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
			# Single-quoted string, possibly containing escape sequences
			(r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

			# 'def' followed by an identifier
			(r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
			# 'class' followed by an identifier
			(r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

			# From '#' until a newline
			(r'#[^\n]*', 0, STYLES['comment']),

			# Numeric literals
			(r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
			(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
		]

		# Build a QRegExp for each pattern
		self.rules = [(QRegExp(pat), index, fmt)
			for (pat, index, fmt) in rules]


	def highlightBlock(self, text):
		"""Apply syntax highlighting to the given block of text.
		"""
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				# We actually want the index of the nth match
				index = expression.pos(nth)
				length = len(expression.cap(nth))
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line strings
		in_multiline = self.match_multiline(text, *self.tri_single)
		if not in_multiline:
			in_multiline = self.match_multiline(text, *self.tri_double)


	def match_multiline(self, text, delimiter, in_state, style):
		"""Do highlighting of multi-line strings. ``delimiter`` should be a
		``QRegExp`` for triple-single-quotes or triple-double-quotes, and
		``in_state`` should be a unique integer to represent the corresponding
		state changes when inside those strings. Returns True if we're still
		inside a multi-line string when this function is finished.
		"""
		# If inside triple-single quotes, start at 0
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		# Otherwise, look for the delimiter on this line
		else:
			start = delimiter.indexIn(text)
			# Move past this match
			add = delimiter.matchedLength()

		# As long as there's a delimiter match on this line...
		while start >= 0:
			# Look for the ending delimiter
			end = delimiter.indexIn(text, start + add)
			# Ending delimiter on this line?
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			# No; multi-line string
			else:
				self.setCurrentBlockState(in_state)
				length = text.length() - start + add
			# Apply formatting
			self.setFormat(start, length, style)
			# Look for the next match
			start = delimiter.indexIn(text, start + length)

		# Return True if still inside a multi-line string, False otherwise
		if self.currentBlockState() == in_state:
			return True
		else:
			return False
#SYNTAX BITIS

class FileWindow(QMainWindow):
	
	def __init__(self, parent):
		
		super(FileWindow, self).__init__(parent)
		
		layout = QVBoxLayout()
		
		self.combo = QComboBox(self)
		self.button_down = QPushButton(self)
		self.button_down.setText("Download")
		
		layout.addWidget(self.combo)
		layout.addWidget(self.button_down)
		
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		
		self.button_down.clicked.connect(self.download_file)
		
	def download_file(self):
		url = "http://127.0.0.1:5000/return-files/" + self.combo.currentText()
		print(url)
		try:
			r = requests.get(url, allow_redirects=True)
		except requests.exceptions.RequestException as err:
			QMessageBox.about(self, "Status", str(err))
		else:
			filename = "downloads/" + self.combo.currentText()
			f = open(filename, 'wb')
			f.write(r.content)
			filepath = os.path.abspath(f.name)
			QMessageBox.about(self, "Status", "Download Complete")
			f.close()
			self.parent().pseudo_open(filepath)
		self.close()
		
class MainWindow(QMainWindow):

	def __init__(self, *args, **kwargs):

		super(MainWindow, self).__init__(*args, **kwargs)

		#log dosyalari icin isimlendirme
		self.log_time = datetime.now()
		self.log_time_string = self.log_time.strftime("%d.%m.%Y %H.%M.%S")
		
		#Metin kutusu, dugmeler, ve layout olusturma
		layout = QVBoxLayout()
		layout2 = QHBoxLayout()
		self.editor = QPlainTextEdit()
		self.editor.installEventFilter(self)
		self.button1 = QPushButton("Light mode")
		self.button2 = QPushButton("Dark mode")
		self.button1.setStyleSheet("background-color: white;  color:black; border: 1px solid gray; padding:5px 10px")
		self.button2.setStyleSheet("background-color: black;  color:white; border: 1px solid gray; padding:5px 10px")

		#Font belirleme
		fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
		fixedfont.setPointSize(12)
		self.editor.setFont(fixedfont)

		#Highlighter
		self.highlighter = PythonHighlighter(self.editor.document())
		
		#Default olarak yolu bos yapma
		self.path = None

		#Layouta metin kutusunu ve butonu ekleme
		layout.addWidget(self.editor)
		layout2.addWidget(self.button1)
		layout2.addWidget(self.button2)
		layout.addLayout(layout2)

		#Ana widget ekleme, layoutu bu widgeta ekleme, ve metin kutusunu bu widgeta yerlestirme
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		
		#Durum cubugu ekleme
		self.status = QStatusBar()
		self.setStatusBar(self.status)
		
		#Toolbar ve Menu ekleme
		file_toolbar = QToolBar("File")
		file_toolbar.setIconSize(QSize(14, 14))
		self.addToolBar(file_toolbar)
		file_menu = self.menuBar().addMenu("&File")
		
		#Hata kayit
		error_check_action = QAction(QIcon(os.path.join('images', 'cloudup.svg')), "Error_Check", self)
		error_check_action.setStatusTip("Upload code to cloud")
		error_check_action.triggered.connect(self.error_check)
		error_check_action.triggered.connect(self.log_menu)
		file_menu.addAction(error_check_action)
		
		#Cloud list aksiyonu
		cloud_down_action = QAction(QIcon(os.path.join('images', 'cloud_down.svg')), "cloud_down", self)
		cloud_down_action.setStatusTip("List files on cloud")
		cloud_down_action.triggered.connect(self.cloud_down)
		cloud_down_action.triggered.connect(self.log_menu)
		file_menu.addAction(cloud_down_action)
		
		#Cloud save aksiyonu
		cloud_up_action = QAction(QIcon(os.path.join('images', 'cloudup.svg')), "Cloud_Up", self)
		cloud_up_action.setStatusTip("Upload code to cloud")
		cloud_up_action.triggered.connect(self.cloud_up)
		cloud_up_action.triggered.connect(self.log_menu)
		file_menu.addAction(cloud_up_action)
		
		#Komut calistirma, toolbara ekleme, ve fonksiyona baglama
		run_action = QAction(QIcon(os.path.join('images', 'run.svg')), "Run", self)
		run_action.setStatusTip("Run the code")
		run_action.triggered.connect(self.run_file)
		run_action.triggered.connect(self.log_menu)
		file_toolbar.addAction(run_action)

		#Dosya acma islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		#Icon kodu olmadan kod nedense calismiyor, ama verilen yerde icon dosyasi yoksa bile kod calisiyor
		open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
		open_file_action.setStatusTip("Open file")
		open_file_action.triggered.connect(self.file_open)
		open_file_action.triggered.connect(self.log_menu)
		file_menu.addAction(open_file_action)
		file_toolbar.addAction(open_file_action)

		#Dosya kaydetme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
		save_file_action.setStatusTip("Save current page")
		save_file_action.triggered.connect(self.file_save)
		save_file_action.triggered.connect(self.log_menu)
		file_menu.addAction(save_file_action)
		file_toolbar.addAction(save_file_action)

		#Dosya farkli kaydetme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
		saveas_file_action.setStatusTip("Save current page to specified file")
		saveas_file_action.triggered.connect(self.file_saveas)
		saveas_file_action.triggered.connect(self.log_menu)
		file_menu.addAction(saveas_file_action)
		file_toolbar.addAction(saveas_file_action)

		#Yazdirma islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
		print_action.setStatusTip("Print current page")
		print_action.triggered.connect(self.file_print)
		print_action.triggered.connect(self.log_menu)
		file_menu.addAction(print_action)
		file_toolbar.addAction(print_action)

		#Toolbar'a yeni bir parca ekleme ve ust tarafta yeni bir menu ekleme(edit)       
		edit_toolbar = QToolBar("Edit")
		edit_toolbar.setIconSize(QSize(16, 16))
		self.addToolBar(edit_toolbar)
		edit_menu = self.menuBar().addMenu("&Edit")

		#Geri alma islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
		undo_action.setStatusTip("Undo last change")
		undo_action.triggered.connect(self.editor.undo)
		undo_action.triggered.connect(self.log_menu)
		edit_menu.addAction(undo_action)

		#Tekrar yap islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
		redo_action.setStatusTip("Redo last change")
		redo_action.triggered.connect(self.editor.redo)
		redo_action.triggered.connect(self.log_menu)
		edit_toolbar.addAction(redo_action)
		edit_menu.addAction(redo_action)

		#edit menusune ayirici ekleme
		edit_menu.addSeparator()

		#Kesme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
		cut_action.setStatusTip("Cut selected text")
		cut_action.triggered.connect(self.editor.cut)
		cut_action.triggered.connect(self.log_menu)
		edit_toolbar.addAction(cut_action)
		edit_menu.addAction(cut_action)

		#Kopyalama islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
		copy_action.setStatusTip("Copy selected text")
		copy_action.triggered.connect(self.editor.copy)
		copy_action.triggered.connect(self.log_menu)
		edit_toolbar.addAction(copy_action)
		edit_menu.addAction(copy_action)
		
		#Yapistir islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
		paste_action.setStatusTip("Paste from clipboard")
		paste_action.triggered.connect(self.editor.paste)
		paste_action.triggered.connect(self.log_menu)
		edit_toolbar.addAction(paste_action)
		edit_menu.addAction(paste_action)
		
		#Kopyalama islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
		select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
		select_action.setStatusTip("Select all text")
		select_action.triggered.connect(self.editor.selectAll)
		select_action.triggered.connect(self.log_menu)
		edit_menu.addAction(select_action)
		
		#edit menusune ayirici ekleme
		edit_menu.addSeparator()
		
		#Toggle wrap
		wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
		wrap_action.setStatusTip("Toggle wrap text to window")
		wrap_action.setCheckable(True)
		wrap_action.setChecked(True)
		wrap_action.triggered.connect(self.edit_toggle_wrap)
		wrap_action.triggered.connect(self.log_menu)
		edit_menu.addAction(wrap_action)

		#Button logs and functions
		self.button1.clicked.connect(self.light_theme)
		self.button2.clicked.connect(self.dark_theme)
		self.button1.clicked.connect(self.log_button)
		self.button2.clicked.connect(self.log_button)
		
		timer = QTimer(self)
		timer.timeout.connect(self.update_data)
		timer.start(1000)
		
		#Basligi yenile ve pencereyi goster
		self.update_title()
		self.show()
	
	#Cloud list files
	def cloud_down(self):
		url = 'http://127.0.0.1:5000/list'
		try:
			r = requests.get(url)
		except requests.exceptions.RequestException as err:
			QMessageBox.about(self, "Status", str(err))
		else:
			filelist = r.json()
			self.sec = FileWindow(self)
			for index in filelist:
				self.sec.combo.addItem(filelist[index])
			self.sec.show()
		
	def	error_check(self):
		abs_file_path = "/temp/" + (os.path.basename(self.path) if self.path else "untitled")
		print(abs_file_path)
		tempf = open(abs_file_path, "w+")
		tempf.write(self.editor.toPlainText())
		tempf.close()
		result = define_error(abs_file_path)
		errors = list_to_dict(result, abs_file_path)
		for i in range(len(errors)):
			to_database(errors[i])
		
	#Cloud update
	def cloud_up(self):
		url = 'http://127.0.0.1:5000/upload'
		nameoffile = os.path.basename(self.path) if self.path else "untitled"
		temp_file = open(nameoffile, 'w')
		temp_file.write(self.editor.toPlainText())
		temp_file.close()
		temp_file = open(nameoffile, 'r')
		files = {'file' : temp_file}
		try:
			r = requests.post(url, files = files)
		except requests.exceptions.RequestException as err:
			QMessageBox.about(self, "Status", str(err))
		else:
			QMessageBox.about(self, "Status", "Upload Successful")

	#Light theme
	def light_theme(self):
		self.editor.setStyleSheet("background-color: white; color:black")

	#Dark theme
	def dark_theme(self):
		self.editor.setStyleSheet("background-color: black; color:white")
	
	#Dugmeler icin log fonksiyonu
	def log_button(self):
		if not os.path.exists('log'):
			os.makedirs('log')
		now = datetime.now()
		now_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
		message = self.sender().text()
		log_file = open('log/LOG %s.txt' % self.log_time_string, "a")
		log_line = now_string + ": BUTTON:" + message + "\n"
		log_file.write(log_line)
		log_file.close()

	#Menuler icin log fonskiyonu
	def log_menu(self):
		if not os.path.exists('log'):
			os.makedirs('log')
		now = datetime.now()
		now_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
		message = self.sender().text()
		log_file = open('log/LOG %s.txt' % self.log_time_string, "a")
		log_line = now_string + ": ACTION:" + message + "\n"
		log_file.write(log_line)
		log_file.close()
	
	#Veri guncelleme
	def update_data(self):
		if not os.path.exists('data'):
			os.makedirs('data')
		now = datetime.now()
		now_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
		data_file = open('data/DATA %s.txt' % self.log_time_string, "a")
		data_line = now_string + ": " + str(len(self.editor.toPlainText())) + "\n"
		data_file.write(data_line)
		data_file.close()
	
	#Takip sistemi
	def eventFilter(self, source, event):
		if (event.type() == QEvent.KeyPress and
			source is self.editor):
			now = datetime.now()
			now_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
			if(event.key() == Qt.Key_Tab):
				key_pressed = "TAB"
			elif(event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
				key_pressed = "ENTER"
			elif(event.key() == Qt.Key_Alt):
				key_pressed = "ALT"
			elif(event.key() == Qt.Key_Home):
				key_pressed = "HOME"
			elif(event.key() == Qt.Key_Insert):
				key_pressed = "INSERT"
			elif(event.key() == Qt.Key_End):
				key_pressed = "END"
			elif(event.key() == Qt.Key_Delete):
				key_pressed = "DELETE"
			elif(event.key() == Qt.Key_Control):
				key_pressed = "CTRL"
			elif(event.key() == Qt.Key_Up):
				key_pressed = "UP"
			elif(event.key() == Qt.Key_Down):
				key_pressed = "DOWN"
			elif(event.key() == Qt.Key_Left):
				key_pressed = "LEFT"
			elif(event.key() == Qt.Key_Right):
				key_pressed = "RIGHT"
			elif(event.key() == Qt.Key_Escape):
				key_pressed = "ESC"
			elif(event.key() == Qt.Key_Backspace):
				key_pressed = "BCKSPC"
			else:
				key_pressed = event.text()
			MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.META)
			modifiers = int(event.modifiers())
			if (modifiers and modifiers & MOD_MASK == modifiers and event.key() > 0 and event.key() != Qt.Key_Shift and event.key() != Qt.Key_Alt and event.key() != Qt.Key_Control and event.key() != Qt.Key_Meta):
				key_pressed = QKeySequence(modifiers + event.key()).toString()
			#Tus kombinasyonlarinda modifier tusu logda gozukmesin
			if(event.key() != Qt.Key_Shift and event.key() != Qt.Key_Alt and event.key() != Qt.Key_Control and event.key() != Qt.Key_Meta):
				if not os.path.exists('log'):
					os.makedirs('log')
				log_file = open('log/LOG %s.txt' % self.log_time_string, "a")
				log_line = now_string + " :" + key_pressed + "\n"
				log_file.write(log_line)
				log_file.close()
			return False
		return super(MainWindow, self).eventFilter(source, event)

	
	#Hata belirtme penceresi(?)
	def dialog_critical(self, s):
		dlg = QMessageBox(self)
		dlg.setText(s)
		dlg.setIcon(QMessageBox.Critical)
		dlg.show()

	#Dosya acma fonksiyonu
	def file_open(self):
		path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt) ;; All files (*.*)")

		if path:
			try:
				with open(path, 'rU') as f:
					text = f.read()

			except Exception as e:
				self.dialog_critical(str(e))

			else:
				self.path = path
				self.editor.setPlainText(text)
				self.update_title()

	#experimental
	def pseudo_open(self, path):
		if path:
			try:
				with open(path, 'rU') as f:
					text = f.read()
					print(text)

			except Exception as e:
				self.dialog_critical(str(e))

			else:
				self.path = path
				self.editor.setPlainText(text)
				self.update_title()

	#Kod calistir
	def run_file(self):
		self.file_save()
		if not self.path:
			return #Eger dosya kaydetme iptal olursa ve path bossa komut calismayacak
		command = "py " + self.path + " & pause"
		os.system(command)
	
	#Dosya kaydetme
	def file_save(self):
		if self.path is None:
			# Eger "path = None" ise, yani dosya bir yerde bulunmuyorsa farkli kaydet kullan.
			return self.file_saveas()
		self._save_to_path(self.path)
		
	#Dosya farkli kaydetme
	def file_saveas(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt) ;; All files (*.*)")

		if not path:
			# Dialog islemi iptal olursa path bos olacak
			return

		self._save_to_path(path)

	#Farkli kaydet ve kaydet fonksiyonlarinin icerigi
	def _save_to_path(self, path):
		text = self.editor.toPlainText()
		try:
			with open(path, 'w') as f:
				f.write(text)

		except Exception as e:
			self.dialog_critical(str(e))

		else:
			self.path = path
			self.update_title()

	#Yazdirma islemi
	def file_print(self):
		dlg = QPrintDialog()
		if dlg.exec_():
			self.editor.print_(dlg.printer())

	#Basligin degistigi fonksiyonlarda calistirilan fonskiyon
	def update_title(self):
		self.setWindowTitle("%s - Deneme Editor" % (os.path.basename(self.path) if self.path else "Untitled"))


	def edit_toggle_wrap(self):
		self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

	#Program baslangic
if __name__ == '__main__':

	if not os.path.exists('log'):
		os.makedirs('log')
	if not os.path.exists('data'):
		os.makedirs('data')
	
	app = QApplication(sys.argv)
	app.setApplicationName("Deneme Editor")

	window = MainWindow()
	app.exec_()
