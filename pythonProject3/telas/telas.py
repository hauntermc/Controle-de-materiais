from PyQt5 import QtWidgets
from banco_de_dados import Usuario, session


class TelaCadastro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Usuário')
        self.setGeometry(100, 100, 300, 250)

        layout = QtWidgets.QVBoxLayout()

        self.label_nome = QtWidgets.QLabel('Nome:')
        layout.addWidget(self.label_nome)
        self.entry_nome = QtWidgets.QLineEdit()
        layout.addWidget(self.entry_nome)

        self.label_username = QtWidgets.QLabel('Username:')
        layout.addWidget(self.label_username)
        self.entry_username = QtWidgets.QLineEdit()
        layout.addWidget(self.entry_username)

        self.label_senha = QtWidgets.QLabel('Senha:')
        layout.addWidget(self.label_senha)
        self.entry_senha = QtWidgets.QLineEdit()
        self.entry_senha.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.entry_senha)

        self.label_confirma_senha = QtWidgets.QLabel('Confirme a Senha:')
        layout.addWidget(self.label_confirma_senha)
        self.entry_confirma_senha = QtWidgets.QLineEdit()
        self.entry_confirma_senha.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.entry_confirma_senha)

        self.botao_cadastrar = QtWidgets.QPushButton('Cadastrar')
        self.botao_cadastrar.clicked.connect(self.cadastrar_usuario)
        layout.addWidget(self.botao_cadastrar)

        self.botao_mostrar_usuarios = QtWidgets.QPushButton('Mostrar Usuários')
        self.botao_mostrar_usuarios.clicked.connect(self.mostrar_usuarios)
        layout.addWidget(self.botao_mostrar_usuarios)

        self.setLayout(layout)

    def cadastrar_usuario(self):
        nome = self.entry_nome.text()
        username = self.entry_username.text()
        senha = self.entry_senha.text()
        confirma_senha = self.entry_confirma_senha.text()

        if nome and username and senha:
            if senha == confirma_senha:
                try:
                    novo_usuario = Usuario(nome=nome, username=username, senha=senha)
                    session.add(novo_usuario)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, 'Sucesso', 'Usuário cadastrado com sucesso!')
                    self.entry_nome.clear()
                    self.entry_username.clear()
                    self.entry_senha.clear()
                    self.entry_confirma_senha.clear()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao cadastrar usuário: {e}')
            else:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'As senhas não coincidem.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')




class TelaLogin(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)

        layout = QtWidgets.QVBoxLayout()

        self.label_username = QtWidgets.QLabel('Username:')
        layout.addWidget(self.label_username)
        self.entry_username = QtWidgets.QLineEdit()
        layout.addWidget(self.entry_username)

        self.label_senha = QtWidgets.QLabel('Senha:')
        layout.addWidget(self.label_senha)
        self.entry_senha = QtWidgets.QLineEdit()
        self.entry_senha.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.entry_senha)

        self.botao_login = QtWidgets.QPushButton('Login')
        self.botao_login.clicked.connect(self.login_usuario)
        layout.addWidget(self.botao_login)

        self.setLayout(layout)

    def login_usuario(self):
        username = self.entry_username.text()
        senha = self.entry_senha.text()

        if username and senha:
            usuario = session.query(Usuario).filter_by(username=username, senha=senha).first()
            if usuario:
                QtWidgets.QMessageBox.information(self, 'Sucesso', 'Login bem-sucedido!')
                # Aqui você pode abrir a tela principal ou realizar outra ação após o login
            else:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'Username ou senha incorretos.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')

class TelaMostrarUsuarios(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Usuários Cadastrados')
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.texto = QtWidgets.QTextEdit()
        self.texto.setReadOnly(True)
        layout.addWidget(self.texto)

        self.setLayout(layout)
        self.mostrar_usuarios()

    def mostrar_usuarios(self):
        usuarios = session.query(Usuario).all()
        if usuarios:
            for usuario in usuarios:
                self.texto.append(f'ID: {usuario.id}, Nome: {usuario.nome}, Username: {usuario.username}')
        else:
            self.texto.append('Nenhum usuário encontrado.')