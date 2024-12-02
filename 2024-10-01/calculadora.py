from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout
import sys

class Calculadora(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")
        self.setGeometry(600, 100, 300, 300)  #Posicion al abrir la ventana y tamaño

        self.resultado = QLineEdit()
        layout = QGridLayout()
        layout.addWidget(self.resultado, 0, 0, 1, 4)  #Cambio el número de columnas a 4

        nombre_boton = [
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            ["0", "/", ".", "C"]]

        # Añadir componentes
        for i in range(4):
            for j in range(4):
                boton = QPushButton(nombre_boton[i][j])
                layout.addWidget(boton, i+1, j)  #Cambié para que comience desde la fila 1
                boton.clicked.connect(self.press_button)

        # Añadir el botón "=" en la fila 5
        boton_igual = QPushButton("=")
        layout.addWidget(boton_igual, 5, 0, 1, 4)  #Ocupa 1 fila y 4 columnas
        boton_igual.clicked.connect(self.press_button)

        self.setLayout(layout)

    def press_button(self):
        sender = self.sender()
        if sender.text() == "=":
            self.resultado.setText(str(eval(self.resultado.text())))
        elif sender.text() == "C":
            self.resultado.clear()
        else:
            self.resultado.setText(self.resultado.text() + sender.text())

    def teclaEnter(self, event):
        if event.key() == 16777220:
            self.press_button()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculadora()
    calc.show()
    sys.exit(app.exec())
