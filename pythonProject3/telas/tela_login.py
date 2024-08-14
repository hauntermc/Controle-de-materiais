from PyQt5 import QtWidgets, QtGui, QtCore
import bcrypt
from banco_de_dados import session, Usuario

class TelaLogin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)
        self.init_ui()
        self.apply_styles()
        self.center()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        login_button = QtWidgets.QPushButton('Login')
        login_button.clicked.connect(self.check_login)

        layout.addWidget(QtWidgets.QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QtWidgets.QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f8ff; /* Background color */
            }
            QLabel {
                font: 14px 'Segoe UI'; /* Font style */
                color: #003366; /* Text color */
            }
            QLineEdit {
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #003366;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00509e;
            }
            QPushButton:pressed {
                background-color: #001f3f;
            }
        """)

    def center(self):
        # Obtém o tamanho da tela
        screen_rect = QtWidgets.QApplication.desktop().availableGeometry()
        screen_center = screen_rect.center()

        # Obtém o tamanho da janela
        window_rect = self.frameGeometry()

        # Calcula a posição da janela para centralizar na tela
        window_rect.moveCenter(screen_center)

        # Define a posição e o tamanho da janela
        self.move(window_rect.topLeft())

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Buscar o usuário no banco de dados
        user = session.query(Usuario).filter_by(username=username).first()

        if user and self.verify_password(password, user.senha):
            self.accept()  # Permite o login
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Credenciais inválidas!')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        # Verificar a senha fornecida com o hash armazenado
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
