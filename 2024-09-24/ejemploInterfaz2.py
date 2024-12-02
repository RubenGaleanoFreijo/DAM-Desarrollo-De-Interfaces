from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import QSize, Qt
import sys

class miVentana(QMainWindow):    
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("Mi Ventana")
        button1 = QPushButton("Mi Boton 1")
        button2 = QPushButton("Mi Boton 2")
        self.setCentralWidget(button1)
        self.setCentralWidget(button2)

app = QApplication(sys.argv)
ventana = miVentana()

ventana.show()
app.exec()