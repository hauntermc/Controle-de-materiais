from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from banco_de_dados import Tecnico, session

class TelaMostrarTecnicos(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #e0f7fa;")  # Fundo azul claro

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Nome', 'Matrícula', 'Telefone'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)  # Remove foco visual ao clicar
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #b0bec5;
                border-radius: 5px;
                padding: 10px;
                gridline-color: #b0bec5;
                font-size: 14px;
                color: #00796b;
            }
            QHeaderView::section {
                background-color: #b3e5fc;
                color: #000000;
                font-weight: bold;
                border: 1px solid #b0bec5;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 8px;
                outline: none; /* Remove o pontilhado ao redor dos itens */
            }
            QTableWidget::item:selected {
                background-color: #b3e5fc;
                color: #004d40;
                outline: none; /* Remove o pontilhado ao redor dos itens selecionados */
            }
            QTableWidget::focus {
                outline: none; /* Remove o foco visual da tabela */
                border: none; /* Remove qualquer borda */
            }
            QTableWidget QTableCornerButton::section {
                border: none;
                background-color: #b3e5fc;
            }
        """)

        self.carregar_dados()

        layout.addWidget(self.table)

        self.refresh_button = QPushButton('Atualizar')
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #03a9f4;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0288d1;
            }
        """)
        self.refresh_button.clicked.connect(self.carregar_dados)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.setWindowTitle('Mostrar Técnicos')
        self.setGeometry(200, 100, 500, 300)

    def carregar_dados(self):
        self.table.setRowCount(0)  # Limpa a tabela antes de carregar novos dados

        try:
            tecnicos = session.query(Tecnico).all()

            for row_number, tecnico in enumerate(tecnicos):
                self.table.insertRow(row_number)
                self.table.setItem(row_number, 0, QTableWidgetItem(tecnico.nome))
                self.table.setItem(row_number, 1, QTableWidgetItem(tecnico.matricula))
                self.table.setItem(row_number, 2, QTableWidgetItem(tecnico.telefone))

        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao carregar dados: {e}')


# Código de execução para testar a tela
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = TelaMostrarTecnicos()
    window.show()
    sys.exit(app.exec_())
