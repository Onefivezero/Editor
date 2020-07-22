from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from datetime import datetime

import os
import sys

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
        self.button1 = QPushButton("Buton1")
        self.button2 = QPushButton("Buton2")

        #Font belirleme
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

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

        #Komut calistirma, toolbara ekleme, ve fonksiyona baglama
        run_action = QAction(QIcon(os.path.join('images', 'run.svg')), "Run", self)
        run_action.setStatusTip("Run the code")
        run_action.triggered.connect(self.run_file)
        file_toolbar.addAction(run_action)

        #Dosya acma islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        #Icon kodu olmadan kod nedense calismiyor, ama verilen yerde icon dosyasi yoksa bile kod calisiyor
        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        #Dosya kaydetme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        #Dosya farkli kaydetme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        #Yazdirma islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
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
        edit_menu.addAction(undo_action)

        #Tekrar yap islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        #edit menusune ayirici ekleme
        edit_menu.addSeparator()

        #Kesme islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        #Kopyalama islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        #Yapistir islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        #Kopyalama islemi ekleme, bu islemi toolbar ve menuye baglama, ve bu islemi bir fonksiyona baglama
        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        #edit menusune ayirici ekleme
        edit_menu.addSeparator()

        #Toggle wrap
        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(1000)
        
        #Basligi yenile ve pencereyi goster
        self.update_title()
        self.show()

    #Veri guncelleme
    def update_data(self):
        now = datetime.now()
        now_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")
        data_file = open('DATA %s.txt' % self.log_time_string, "a")
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
                log_file = open('LOG %s.txt' % self.log_time_string, "a")
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
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

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

    #Kod calistir
    def run_file(self):
        self.file_saveas()
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
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

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

    
    app = QApplication(sys.argv)
    app.setApplicationName("Deneme Editor")

    window = MainWindow()
    app.exec_()
