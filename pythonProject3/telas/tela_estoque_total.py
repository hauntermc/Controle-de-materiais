from PyQt5 import QtWidgets, QtGui, QtCore
from banco_de_dados import session, Material
from sqlalchemy import func

class TelaEstoque(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Estoque Total')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #e0f7fa;")  # Azul claro
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Adicionar tabela
        self.tabela_estoque = QtWidgets.QTableWidget()
        self.tabela_estoque.setColumnCount(5)
        self.tabela_estoque.setHorizontalHeaderLabels(['Nome do Produto', 'Quantidade', 'Valor Mínimo', 'Status', 'Salvar'])
        self.tabela_estoque.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tabela_estoque.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #b0bec5;
            }
            QHeaderView::section {
                background-color: #b3e5fc;
                border: 1px solid #b0bec5;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)

        # Botão para atualizar a tabela
        atualizar_button = QtWidgets.QPushButton('Atualizar Estoque')
        atualizar_button.setFixedHeight(25)
        atualizar_button.setFixedWidth(150)
        atualizar_button.setStyleSheet("background-color: #03a9f4; color: white; border-radius: 5px;")
        atualizar_button.clicked.connect(self.carregar_dados)

        # Botões para filtrar
        self.urgente_button = QtWidgets.QPushButton('Mostrar Produtos Urgentes')
        self.urgente_button.setFixedWidth(150)
        self.urgente_button.setFixedHeight(25)
        self.urgente_button.setStyleSheet("background-color: #ff5722; color: white; border-radius: 5px;")
        self.urgente_button.clicked.connect(lambda: self.filtrar_status('Urgente'))

        self.alerta_button = QtWidgets.QPushButton('Mostrar Produtos em Alerta')
        self.alerta_button.setFixedWidth(150)
        self.alerta_button.setFixedHeight(25)
        self.alerta_button.setStyleSheet("background-color: #ffeb3b; color: black; border-radius: 5px;")
        self.alerta_button.clicked.connect(lambda: self.filtrar_status('Alerta'))

        layout.addWidget(atualizar_button)
        layout.addWidget(self.urgente_button)
        layout.addWidget(self.alerta_button)
        layout.addWidget(self.tabela_estoque)
        self.setLayout(layout)

        # Carregar dados inicialmente
        self.carregar_dados()

    def carregar_dados(self):
        try:
            # Limpar dados existentes
            self.tabela_estoque.setRowCount(0)
            self.materiais_dados = []  # Inicializar a lista

            # Obter dados agregados dos materiais
            materiais = session.query(
                Material.nome,
                func.sum(Material.quantidade).label('total_quantidade'),
                func.min(Material.valor_minimo).label('min_valor_minimo')
            ).group_by(Material.nome).all()

            for material in materiais:
                row_position = self.tabela_estoque.rowCount()
                self.tabela_estoque.insertRow(row_position)

                # Nome do Produto
                self.tabela_estoque.setItem(row_position, 0, QtWidgets.QTableWidgetItem(material.nome))

                # Quantidade total
                quantidade_item = QtWidgets.QTableWidgetItem(str(material.total_quantidade))
                self.tabela_estoque.setItem(row_position, 1, quantidade_item)

                # Valor Mínimo
                valor_minimo_item = QtWidgets.QLineEdit()
                valor_minimo_item.setText(str(material.min_valor_minimo) if material.min_valor_minimo else '')  # Define o valor mínimo existente
                valor_minimo_item.textChanged.connect(lambda text, row=row_position: self.atualizar_status(row))
                self.tabela_estoque.setCellWidget(row_position, 2, valor_minimo_item)

                # Status
                status_item = QtWidgets.QTableWidgetItem()
                self.tabela_estoque.setItem(row_position, 3, status_item)

                # Botão de Salvar
                salvar_button = QtWidgets.QPushButton('Salvar')
                salvar_button.setStyleSheet("background-color: #4caf50; color: white; border-radius: 5px;")
                salvar_button.clicked.connect(lambda checked, row=row_position: self.salvar_valor_minimo(row))
                self.tabela_estoque.setCellWidget(row_position, 4, salvar_button)

                # Atualizar cor do status
                self.atualizar_status(row_position)
                # Adicionar dados de status para filtragem
                self.materiais_dados.append({
                    'row': row_position,
                    'nome': material.nome,
                    'quantidade': material.total_quantidade,
                    'valor_minimo': material.min_valor_minimo,
                    'status': self.tabela_estoque.item(row_position, 3).text()
                })
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao carregar dados: {e}')

    def atualizar_status(self, row):
        try:
            valor_minimo_widget = self.tabela_estoque.cellWidget(row, 2)
            if valor_minimo_widget is None:
                return

            valor_minimo_text = valor_minimo_widget.text() if valor_minimo_widget else ''
            valor_minimo = float(valor_minimo_text) if valor_minimo_text else 0

            quantidade_item = self.tabela_estoque.item(row, 1)
            quantidade_text = quantidade_item.text() if quantidade_item else '0'
            quantidade = int(quantidade_text)

            status_item = self.tabela_estoque.item(row, 3)
            if status_item is None:
                status_item = QtWidgets.QTableWidgetItem()
                self.tabela_estoque.setItem(row, 3, status_item)

            if quantidade <= valor_minimo:
                status_item.setBackground(QtGui.QColor('red'))
                status_item.setText('Urgente')
            elif quantidade <= 1.5 * valor_minimo:
                status_item.setBackground(QtGui.QColor('yellow'))
                status_item.setText('Alerta')
            else:
                status_item.setBackground(QtGui.QColor('white'))
                status_item.setText('Normal')

            # Atualizar dados para filtragem
            if row < len(self.materiais_dados):
                self.materiais_dados[row]['status'] = status_item.text()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao atualizar status: {e}')

    def salvar_valor_minimo(self, row):
        try:
            valor_minimo_widget = self.tabela_estoque.cellWidget(row, 2)
            if valor_minimo_widget is None:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'Campo Valor Mínimo não encontrado.')
                return

            valor_minimo_text = valor_minimo_widget.text() if valor_minimo_widget else ''
            valor_minimo = float(valor_minimo_text) if valor_minimo_text else 0

            nome_produto = self.tabela_estoque.item(row, 0).text()
            materiais = session.query(Material).filter_by(nome=nome_produto).all()
            if materiais:
                for material in materiais:
                    # Atualizar o valor mínimo do material
                    material.valor_minimo = valor_minimo
                session.commit()

                # Atualizar o status após a mudança do valor mínimo
                self.atualizar_status(row)

                QtWidgets.QMessageBox.information(self, 'Sucesso', 'Valor mínimo salvo com sucesso!')
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Valor mínimo inválido.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao salvar valor mínimo: {e}')

    def filtrar_status(self, status_filtrado):
        try:
            # Limpar tabela
            self.tabela_estoque.setRowCount(0)

            # Recarregar dados filtrados
            for dado in self.materiais_dados:
                if dado['status'] == status_filtrado:
                    row = self.tabela_estoque.rowCount()
                    self.tabela_estoque.insertRow(row)

                    # Recriar linha na tabela
                    self.tabela_estoque.setItem(row, 0, QtWidgets.QTableWidgetItem(dado['nome']))
                    self.tabela_estoque.setItem(row, 1, QtWidgets.QTableWidgetItem(str(dado['quantidade'])))

                    valor_minimo_item = QtWidgets.QLineEdit()
                    valor_minimo_item.setText(str(dado['valor_minimo']) if dado['valor_minimo'] else '')
                    self.tabela_estoque.setCellWidget(row, 2, valor_minimo_item)

                    status_item = QtWidgets.QTableWidgetItem(dado['status'])
                    if dado['status'] == 'Urgente':
                        status_item.setBackground(QtGui.QColor('red'))
                    elif dado['status'] == 'Alerta':
                        status_item.setBackground(QtGui.QColor('yellow'))
                    else:
                        status_item.setBackground(QtGui.QColor('white'))
                    self.tabela_estoque.setItem(row, 3, status_item)

                    salvar_button = QtWidgets.QPushButton('Salvar')
                    salvar_button.setStyleSheet("background-color: #4caf50; color: white; border-radius: 5px;")
                    salvar_button.clicked.connect(lambda checked, row=row: self.salvar_valor_minimo(row))
                    self.tabela_estoque.setCellWidget(row, 4, salvar_button)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Erro ao filtrar produtos: {e}')
