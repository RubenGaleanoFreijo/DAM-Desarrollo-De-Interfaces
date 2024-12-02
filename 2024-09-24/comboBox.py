import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QApplication, QVBoxLayout, QWidget, QComboBox

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        desplegable = QComboBox()
        self.setCentralWidget(desplegable)
        desplegable.addItems(("Opcion 1", "Opcion 2"))
        desplegable.currentIndexChanged.connect(self.mostrarIndice)
        desplegable.currentTextChanged.connect(self.mostrarTexto)
    
    def mostrarIndice(self, indice):
        print(f"indice seleccionado: {indice}")

    def mostrarTexto(self, texto):
        print(f"Texto seleccionado: {texto}")
    

app = QApplication(sys.argv)
window = mainWindow()
window.show()

app.exec()