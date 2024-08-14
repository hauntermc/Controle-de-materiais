from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from banco_de_dados import Material, RetiradaMaterial, session

class MaterialTableModel(QAbstractTableModel):
    def __init__(self, materials, parent=None):
        super().__init__(parent)
        self.materials = materials

    def rowCount(self, parent=QModelIndex()):
        return len(self.materials)

    def columnCount(self, parent=QModelIndex()):
        return 7  # Alterado para 7 colunas: ID, Nome, Preço, Nota Fiscal, Quantidade, Patrimônio, Data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            material = self.materials[index.row()]
            if index.column() == 0:
                return material.id
            elif index.column() == 1:
                return material.nome
            elif index.column() == 2:
                return material.preco
            elif index.column() == 3:
                return material.nota_fiscal
            elif index.column() == 4:
                return material.quantidade
            elif index.column() == 5:
                return material.patrimonio
            elif index.column() == 6:
                return material.data.strftime('%Y-%m-%d %H:%M:%S')

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            headers = ['ID', 'Nome', 'Preço', 'Nota Fiscal', 'Quantidade', 'Patrimônio', 'Data']
            if orientation == Qt.Horizontal:
                return headers[section]

    def removeRow(self, row, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        del self.materials[row]
        self.endRemoveRows()

    def update_data(self, materials):
        self.beginResetModel()
        self.materials = materials
        self.endResetModel()

class TelaMostrarMateriais(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Cor de fundo azul clara */
                font-family: Arial, sans-serif;
            }
            QLineEdit, QTableView {
                background-color: #ffffff;
                border: 2px solid #003366;
                padding: 8px;
                border-radius: 5px;
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

        search_layout = QHBoxLayout()
        self.search_label = QLabel('Pesquisar:')
        self.search_input = QLineEdit()
        self.search_button = QPushButton('Buscar')
        self.search_button.clicked.connect(self.pesquisar_material)

        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)

        self.table_view = QTableView()

        # Obter materiais do banco de dados
        self.materials = session.query(Material).all()
        self.model = MaterialTableModel(self.materials)
        self.table_view.setModel(self.model)

        layout.addWidget(self.table_view)

        botoes_layout = QHBoxLayout()

        self.delete_button = QPushButton('Excluir')
        self.delete_button.clicked.connect(self.excluir_material)
        botoes_layout.addWidget(self.delete_button)

        self.close_button = QPushButton('Fechar')
        self.close_button.clicked.connect(self.close)
        botoes_layout.addWidget(self.close_button)

        layout.addLayout(botoes_layout)

        self.setLayout(layout)
        self.setWindowTitle('Materiais Registrados')
        self.setGeometry(100, 100, 800, 600)  # Defina o tamanho da tela conforme necessário

    def excluir_material(self):
        index = self.table_view.currentIndex()
        if index.isValid():
            material_id = self.model.materials[index.row()].id
            material = session.query(Material).get(material_id)
            if material:
                # Verificar se existem retiradas associadas
                retiradas = session.query(RetiradaMaterial).filter_by(material_id=material_id).all()
                if retiradas:
                    # Verificar se o material já foi retornado
                    material_retornado = all(retirada.retorno for retirada in retiradas)
                    if not material_retornado:
                        QMessageBox.warning(self, 'Erro',
                                            'Não é possível excluir este material, pois ele está associado a uma ou mais retiradas não retornadas.')
                        return

                # Confirmação de exclusão
                reply = QMessageBox.question(self, 'Confirmação de Exclusão',
                                             f'Tem certeza de que deseja excluir o material "{material.nome}"?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        session.delete(material)
                        session.commit()
                        self.model.removeRow(index.row())
                        QMessageBox.information(self, 'Sucesso', 'Material excluído com sucesso!')
                    except Exception as e:
                        session.rollback()
                        QMessageBox.critical(self, 'Erro', f'Erro ao excluir o material: {str(e)}')
            else:
                QMessageBox.warning(self, 'Erro', 'Material não encontrado!')
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum material selecionado!')

    def pesquisar_material(self):
        termo_pesquisa = self.search_input.text()
        try:
            if termo_pesquisa:
                materiais_filtrados = session.query(Material).filter(
                    Material.nome.ilike(f'%{termo_pesquisa}%') |
                    Material.nota_fiscal.ilike(f'%{termo_pesquisa}%')
                ).all()
                if materiais_filtrados:
                    self.model.update_data(materiais_filtrados)
                else:
                    QMessageBox.information(self, 'Sem Resultados', 'Nenhum material encontrado.')
            else:
                self.model.update_data(session.query(Material).all())
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro durante a busca: {str(e)}')
