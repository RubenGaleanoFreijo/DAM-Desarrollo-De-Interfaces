import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QApplication, QVBoxLayout, QWidget

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()  
        widget = QWidget()      

        label1 = QLabel("Hola")
        label1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label1)  

        label2 = QLabel("Hola")
        label2.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        layout.addWidget(label2)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = mainWindow()
window.show()

app.exec()
