from PyQt5 import QtWidgets, QtGui
from banco_de_dados import session, Fornecedor

class TelaFornecedores(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lista de Fornecedores')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Estilo moderno com cor azul clara
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Cor de fundo azul clara */
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
                border: none;
            }
            QPushButton:hover {
                background-color: #0055a5;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 2px solid #003366;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #003366;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QTableWidgetItem {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
        """)

        # Adicionar tabela
        self.tabela_fornecedores = QtWidgets.QTableWidget()
        self.tabela_fornecedores.setColumnCount(2)
        self.tabela_fornecedores.setHorizontalHeaderLabels(['Nome do Fornecedor', 'CNPJ'])
        self.tabela_fornecedores.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Definir largura das colunas
        self.tabela_fornecedores.setColumnWidth(0, 300)  # Ajuste o valor conforme necessário
        self.tabela_fornecedores.setColumnWidth(1, 200)  # Ajuste o valor conforme necessário

        # Botão para atualizar a tabela
        atualizar_button = QtWidgets.QPushButton('Atualizar Fornecedores')
        atualizar_button.clicked.connect(self.carregar_dados)

        layout.addWidget(atualizar_button)
        layout.addWidget(self.tabela_fornecedores)
        self.setLayout(layout)

        # Carregar dados inicialmente
        self.carregar_dados()

    def carregar_dados(self):
        try:
            # Limpar dados existentes
            self.tabela_fornecedores.setRowCount(0)

            # Obter dados dos fornecedores
            fornecedores = session.query(Fornecedor).all()

            for fornecedor in fornecedores:
                row_position = self.tabela_fornecedores.rowCount()
                self.tabela_fornecedores.insertRow(row_position)

                # Nome do Fornecedor
                self.tabela_fornecedores.setItem(row_position, 0, QtWidgets.QTableWidgetItem(fornecedor.nome))

                # CNPJ
                self.tabela_fornecedores.setItem(row_position, 1, QtWidgets.QTableWidgetItem(fornecedor.cnpj))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao carregar dados: {e}')
