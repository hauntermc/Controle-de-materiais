from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from banco_de_dados import Fornecedor, session

class TelaRegistroFornecedor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Registrar Fornecedor')
        self.resize(400, 100)
        self.setStyleSheet("background-color: #eaf4f4;")  # Cor de fundo azul clara

        layout = QFormLayout()

        # Campo para Nome
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText('Digite o nome do fornecedor')
        self.nome_input.setStyleSheet(
            "border: 1px solid #007bff; border-radius: 5px; padding: 10px; background-color: white;")
        layout.addRow('Nome:', self.nome_input)

        # Campo para CNPJ com máscara de entrada
        self.cnpj_input = QLineEdit()
        self.cnpj_input.setInputMask('00.000.000/0000-00')  # Máscara para o formato do CNPJ
        self.cnpj_input.setPlaceholderText('Digite o CNPJ do fornecedor')
        self.cnpj_input.setStyleSheet(
            "border: 1px solid #007bff; border-radius: 5px; padding: 10px; background-color: white;")
        layout.addRow('CNPJ:', self.cnpj_input)

        # Botão de Salvar
        self.save_button = QPushButton('Salvar')
        self.save_button.setStyleSheet(
            "background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 10px; font-weight: bold;")
        self.save_button.clicked.connect(self.salvar_fornecedor)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def salvar_fornecedor(self):
        nome = self.nome_input.text().strip()
        cnpj = self.cnpj_input.text().strip()

        if not nome:
            QMessageBox.warning(self, 'Erro', 'O campo Nome é obrigatório.')
            return

        # Remove a máscara para validação
        cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
        if len(cnpj) != 14:
            QMessageBox.warning(self, 'Erro', 'O CNPJ deve conter 14 dígitos numéricos.')
            return

        try:
            novo_fornecedor = Fornecedor(nome=nome, cnpj=self.cnpj_input.text())
            session.add(novo_fornecedor)
            session.commit()
            QMessageBox.information(self, 'Sucesso', 'Fornecedor registrado com sucesso!')
            self.nome_input.clear()
            self.cnpj_input.clear()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, 'Erro', f'Erro ao registrar fornecedor: {e}')
