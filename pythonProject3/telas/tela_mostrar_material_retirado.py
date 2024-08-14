from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox
from banco_de_dados import session, RetiradaMaterial, Material


class TelaMateriaisRetirados(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Materiais Retirados')
        self.setGeometry(200, 100, 1400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Estilo moderno com cor azul clara
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Cor de fundo azul clara */
                font-family: Arial, sans-serif;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 2px solid #003366;
                padding: 8px;
                border-radius: 5px;
                gridline-color: #003366;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #003366;
                color: white;
                padding: 8px;
                border: none;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #0055a5;
            }
            QLabel {
                color: #003366;
                font-weight: bold;
                font-size: 12pt;
            }
        """)

        # Botão de Atualizar
        self.btn_atualizar = QPushButton('Atualizar')
        self.btn_atualizar.clicked.connect(self.load_data)
        layout.addWidget(self.btn_atualizar)

        # Tabela para mostrar materiais retirados
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)  # Adiciona uma coluna para o botão de exclusão
        self.table.setHorizontalHeaderLabels(
            ['ID', 'OS', 'Nome do Material', 'Quantidade', 'Nome do Técnico', 'Data Retirada', 'Patrimônio', 'Local',
             'Retornado', 'Excluir'])
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)

        # Adicionar tabela ao layout
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Carregar dados na tabela
        self.load_data()

    def load_data(self):
        try:
            # Carrega todos os materiais retirados, independentemente de terem sido retornados
            materiais_retirados = session.query(RetiradaMaterial).join(RetiradaMaterial.material).all()

            self.table.setRowCount(len(materiais_retirados))
            for row, retirada in enumerate(materiais_retirados):
                self.table.setItem(row, 0, QTableWidgetItem(str(retirada.id)))
                self.table.setItem(row, 1, QTableWidgetItem(retirada.ordem_servico))
                self.table.setItem(row, 2, QTableWidgetItem(retirada.material.nome))
                self.table.setItem(row, 3, QTableWidgetItem(str(retirada.quantidade)))
                self.table.setItem(row, 4, QTableWidgetItem(retirada.tecnico_nome))
                self.table.setItem(row, 5, QTableWidgetItem(retirada.data_retirada.strftime('%Y-%m-%d %H:%M:%S')))
                self.table.setItem(row, 6, QTableWidgetItem(retirada.patrimonio))
                self.table.setItem(row, 7, QTableWidgetItem(retirada.local_utilizacao))
                retornado_text = 'Sim' if retirada.retornado else 'Não'
                self.table.setItem(row, 8, QTableWidgetItem(retornado_text))

                # Adiciona o botão de exclusão na última coluna
                delete_button = QPushButton('Excluir')
                delete_button.clicked.connect(lambda _, r=row: self.excluir_material(r))
                self.table.setCellWidget(row, 9, delete_button)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao carregar os dados: {str(e)}')

    def excluir_material(self, row):
        try:
            item = self.table.item(row, 0)  # Coluna 0 contém o ID
            if item:
                retirada_id = int(item.text())
                retirada = session.query(RetiradaMaterial).get(retirada_id)
                if retirada:
                    if not retirada.retornado:
                        QMessageBox.warning(self, 'Erro', 'Não é possível excluir um material que não foi retornado.')
                        return

                    # Confirmação de exclusão
                    reply = QMessageBox.question(self, 'Confirmação de Exclusão',
                                                 f'Tem certeza de que deseja excluir o material retornado com ID {retirada_id}?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        try:
                            session.delete(retirada)
                            session.commit()
                            self.table.removeRow(row)
                            QMessageBox.information(self, 'Sucesso', 'Material excluído com sucesso!')
                        except Exception as e:
                            session.rollback()
                            QMessageBox.critical(self, 'Erro', f'Erro ao excluir o material: {str(e)}')
                else:
                    QMessageBox.warning(self, 'Erro', 'Retirada não encontrada!')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao excluir o material: {str(e)}')
