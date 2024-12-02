import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout
 
class Usuario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log in")
        self.setGeometry(600, 300, 300, 150)
 
        label_usuario = QLabel("Usuario:")
        label_contrasenia = QLabel("Contraseña:")
        
        self.usuario = QLineEdit()
        self.contrasenia = QLineEdit()
        self.contrasenia.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.clicked.connect(self.enviar_datos)
 
        layout = QGridLayout()
        layout.addWidget(label_usuario, 0, 0)
        layout.addWidget(self.usuario, 1, 0)
        layout.addWidget(label_contrasenia, 2, 0)
        layout.addWidget(self.contrasenia, 3, 0)
        layout.addWidget(self.boton_enviar, 4, 0)
 
        self.setLayout(layout)
 
    def enviar_datos(self):
        usuario = self.usuario.text()
        contrasenia = self.contrasenia.text()
        print(f"Usuario: {usuario}, Contraseña: {contrasenia}")
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Usuario()
    ventana.show()
    sys.exit(app.exec())
 