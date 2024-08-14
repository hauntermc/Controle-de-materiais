from PyQt5 import QtWidgets
import bcrypt
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

        self.setLayout(layout)

    def cadastrar_usuario(self):
        nome = self.entry_nome.text()
        username = self.entry_username.text()
        senha = self.entry_senha.text()
        confirma_senha = self.entry_confirma_senha.text()

        if nome and username and senha:
            if senha == confirma_senha:
                try:
                    # Verifica se o username já existe
                    usuario_existente = session.query(Usuario).filter_by(username=username).first()
                    if usuario_existente:
                        QtWidgets.QMessageBox.warning(self, 'Erro', 'Username já existe.')
                        return

                    # Criptografa a senha antes de salvar
                    hash_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

                    novo_usuario = Usuario(nome=nome, username=username, senha=hash_senha)
                    session.add(novo_usuario)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, 'Sucesso', 'Usuário cadastrado com sucesso!')
                    self.entry_nome.clear()
                    self.entry_username.clear()
                    self.entry_senha.clear()
                    self.entry_confirma_senha.clear()
                except Exception as e:
                    session.rollback()  # Desfaz a transação em caso de erro
                    QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao cadastrar usuário: {e}')
            else:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'As senhas não coincidem.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')
