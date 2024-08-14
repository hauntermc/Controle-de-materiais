from PyQt5 import QtWidgets, QtGui, QtCore
from banco_de_dados import Usuario, session


class TelaMostrarUsuarios(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Usuários Cadastrados')
        self.setGeometry(100, 100, 500, 300)

        layout = QtWidgets.QVBoxLayout()

        # Cria a tabela para mostrar os usuários
        self.tabela = QtWidgets.QTableWidget()
        self.tabela.setColumnCount(3)  # Número de colunas (ID, Nome, Username)
        self.tabela.setHorizontalHeaderLabels(['ID', 'Nome', 'Username'])
        self.tabela.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabela.setFocusPolicy(QtCore.Qt.NoFocus)  # Remove foco visual ao clicar
        layout.addWidget(self.tabela)

        self.setLayout(layout)
        self.mostrar_usuarios()

        self.aplicar_estilo_moderno()

    def mostrar_usuarios(self):
        usuarios = session.query(Usuario).all()
        self.tabela.setRowCount(len(usuarios))  # Define o número de linhas na tabela

        for row, usuario in enumerate(usuarios):
            self.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(str(usuario.id)))
            self.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(usuario.nome))
            self.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(usuario.username))

    def aplicar_estilo_moderno(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e0f7fa; /* Cor de fundo azul claro */
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                background-color: #ffffff; /* Fundo branco para a tabela */
                border: 1px solid #0288d1; /* Borda azul */
                border-radius: 5px;
                gridline-color: #0288d1; /* Cor das linhas da grade */
                font-size: 14px;
                color: #00796b; /* Cor do texto */
            }
            QHeaderView::section {
                background-color: #0288d1; /* Cor de fundo do cabeçalho */
                color: #ffffff; /* Cor do texto do cabeçalho */
                padding: 5px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
                outline: none; /* Remove o pontilhado ao redor dos itens */
                border: none;  /* Remove qualquer borda */
            }
            QTableWidget::item:selected {
                background-color: #b3e5fc; /* Cor de fundo ao selecionar uma linha */
                color: #004d40; /* Cor do texto ao selecionar uma linha */
                outline: none; /* Remove o pontilhado ao redor dos itens selecionados */
            }
            QTableWidget::focus {
                outline: none; /* Remove o foco visual da tabela */
                border: none;  /* Remove qualquer borda */
            }
            QTableWidget QTableCornerButton::section {
                border: none; /* Remove borda do canto superior esquerdo da tabela */
                background-color: #0288d1; /* Cor de fundo do canto superior esquerdo */
            }
        """)

        # Ajusta o tamanho das colunas para se ajustarem ao conteúdo
        self.tabela.resizeColumnsToContents()
        self.tabela.horizontalHeader().setStretchLastSection(True)


# Código de execução para testar a tela
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = TelaMostrarUsuarios()
    window.show()
    sys.exit(app.exec_())
