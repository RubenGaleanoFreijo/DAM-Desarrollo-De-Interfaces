#importamos las librerías necesarias
import sys
import time
import threading
from PyQt6 import QtWidgets, uic

# Carga la interfaz gráfica y conecta los botones
class Ventana(QtWidgets.QMainWindow):
    '''Esta es la clase principal'''
    def __init__(self, padre=None):
        # Inicializa la ventana
        QtWidgets.QMainWindow.__init__(self, padre)
        uic.loadUi("progressBar.ui", self)  # Lee el archivo de QtDesigner

        self.setWindowTitle("Barra de Progreso")  # Título de la ventana

        # Setear la barra de progreso
        self.progressBar
        # Conectar botones a funciones
        self.startButton.clicked.connect(self.empezar)
        self.stopButton.clicked.connect(self.parar)
        self.continueButton.clicked.connect(self.continuar)

        # Variables de control
        self.contador = 0
        self.running = False  # Variable para controlar si la barra está corriendo
        self.x = None  # El hilo se inicializa en None para poder reiniciarlo

    def barra_progreso(self):
        while self.running:
            time.sleep(0.1)

            if self.progressBar.value() < self.progressBar.maximum():
                self.label.setText("Cargando Tabla...")
                self.contador += 20
                self.progressBar.setValue(self.contador)

            elif self.progressBar.value() == 100:
                self.label.setText("Barra Completada")
                time.sleep(2)
                self.contador = 0
                self.progressBar.reset()
                self.label.setText("Cargando Tabla...")

    def empezar(self):
        if self.x is None or not self.x.is_alive():
            self.running = True  # Indicar que el hilo está corriendo
            self.x = threading.Thread(target=self.barra_progreso)
            self.contador = 0
            self.progressBar.reset()
            self.x.start() # Indicar que el hilo continue

    def parar(self):
        self.running = False  # Detener el hilo
        if self.x is not None:
            self.x.join()  # Esperar a que el hilo termine
    
    def continuar(self):
        self.running = True  # Indicar que el hilo está corriendo
        self.x = threading.Thread(target=self.barra_progreso)
        self.x.start() #Indicar que el hilo continue

# Se crea la instancia de la aplicación
app = QtWidgets.QApplication(sys.argv)
# Se crea la instancia de la ventana
miVentana = Ventana()
# Se muestra la ventana
miVentana.show()
# Se entrega el control al sistema operativo
sys.exit(app.exec())
