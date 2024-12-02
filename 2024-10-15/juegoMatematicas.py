import sys
import random
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QDoubleValidator 

# Esta es la clase principal
class Ventana(QtWidgets.QMainWindow):

    def __init__(self, padre=None):
        super().__init__(padre)
        uic.loadUi("juegoMatematicas.ui", self)   # Lee el archivo de QtDesigner

        self.setWindowTitle("Juego de las Matemáticas")   # Título de la ventana

        # Inicializar variables
        self.contador = 0
        self.comprobados = [False] * 10  # Lista para marcar si se han comprobado los resultados
        self.resultados_correctos = []  # Para almacenar los resultados correctos

        # Aplicar el validador para números decimales
        validator = QDoubleValidator()
        for i in range(1, 11):
            resultado_line_edit = getattr(self, f'resultado{i}')
            resultado_line_edit.setValidator(validator)
            resultado_line_edit.textChanged.connect(self.restablecer_color)

        # Conectar el botón con su función
        self.botonComprobar.clicked.connect(self.comprobar)

         # Generar y mostrar operaciones
        self.generar_operaciones()

    def generar_operaciones(self):
         operaciones = []
         for _ in range(10):  # Generar 10 operaciones
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operador = random.choice(['+', '-', '*'])
            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            operaciones.append((f"{num1} {operador} {num2}", resultado))
        
         # Actualizar los QLabel con las operaciones
         for i in range(1, 11):
            getattr(self, f'operacion{i}').setText(operaciones[i - 1][0])

        # Guardar los resultados para su comprobación
         self.resultados_correctos = [op[1] for op in operaciones]

    # Verificar que todas las operaciones estén completadas
    def comprobar(self):
        if not self.todas_operaciones_completadas():
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Por favor, completa todas las operaciones antes de comprobar.")
            return
        else:
            confirmacion = QtWidgets.QMessageBox.question(self, "Confirmación", "¿Estás seguro que quieres finalizar?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if confirmacion == QtWidgets.QMessageBox.StandardButton.No:
                return
            
            
        for i in range(10):
            resultado = getattr(self, f'resultado{i + 1}')
            if resultado.text() == str(self.resultados_correctos[i]):
                if not self.comprobados[i]:  # Solo incrementar si no ha sido comprobado antes
                    resultado.setStyleSheet("color: green;")
                    self.comprobados[i] = True  # Marcar como comprobado
                    self.contador += 10  # Aumentar contador en 10
            else:
                # Si el resultado ha sido comprobado y era correcto, cambiar a rojo y disminuir el contador
                if self.comprobados[i]:
                    resultado.setStyleSheet("color: red;")
                    self.comprobados[i] = False  # Marcar como no comprobado
                    self.contador -= 10 # Disminuir el contador en 10
                 # Si nunca ha sido comprobado y es incorrecto
                else:
                    resultado.setStyleSheet("color: red;")

        #Limita  el contador entre 0 y 100
        self.contador = max(0, min(self.contador, 100))
        self.progressBar.setValue(self.contador)

        if self.progressBar.value() == 100:
            self.enhorabuena.setText("ENHORABUENA")
        else:
            self.enhorabuena.setText("Algo no ha ido bien...")

    # Verifica si todos los campos de resultados están llenos
    def todas_operaciones_completadas(self):
        for i in range(10):
            resultado = getattr(self, f'resultado{i + 1}')
            if resultado.text() == "":
                return False
        return True

    def restablecer_color(self):
        # Restablece el color del QLineEdit que ha cambiado a su estado original, si es necesario
        for i in range(10):
            resultado = getattr(self, f'resultado{i + 1}')
            # Restablecer estilo si el texto está vacío o se está editando
            if resultado.text() == "" or resultado.hasFocus():
                resultado.setStyleSheet("") # Restablece el estilo

# Se crea la instancia de la aplicación
app = QtWidgets.QApplication(sys.argv)
# Se crea la instancia de la ventana
miVentana = Ventana()
# Se muestra la ventana
miVentana.show()
# Se entrega el control al sistema operativo
sys.exit(app.exec())
