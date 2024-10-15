import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIntValidator 

class Ventana(QtWidgets.QMainWindow):
    '''Esta es la clase principal'''
    def __init__(self, padre=None):
        super().__init__(padre)
        uic.loadUi("juegoMatematicas.ui", self)  # Lee el archivo de QtDesigner

        self.setWindowTitle("Juego de las Matemáticas")  # Título de la ventana

        # Inicializar variables
        self.contador = 0
        self.comprobados = [False] * 5  # Lista para marcar si se han comprobado los resultados

        # Aplicar el validador para números decimales
        validator = QIntValidator()
        self.resultado1.setValidator(validator)
        self.resultado2.setValidator(validator)
        self.resultado3.setValidator(validator)
        self.resultado4.setValidator(validator)
        self.resultado5.setValidator(validator)

        # Conectar el boton con su funcion
        self.botonComprobar.clicked.connect(self.comprobar)
        
    def comprobar(self):
        for i in range(1, 6):
            resultado = getattr(self, f'resultado{i}')
            if resultado.text() == "4" and not self.comprobados[i - 1]:
                self.contador += 20
                self.progressBar.setValue(self.contador)
                self.comprobados[i - 1] = True  # Marcar como comprobado
            
            if self.progressBar.value() == 100:
                self.enhorabuena.setText("ENHORABUENA")
erwwrw
# Se crea la instancia de la aplicación
app = QtWidgets.QApplication(sys.argv)
# Se crea la instancia de la ventana
miVentana = Ventana()
# Se muestra la ventana
miVentana.show()
# Se entrega el control al sistema operativo
sys.exit(app.exec())
