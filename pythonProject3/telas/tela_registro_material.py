from PyQt5.QtWidgets import QWidget, QLineEdit, QDoubleSpinBox, QLabel, QSpinBox, QFormLayout, QPushButton, \
    QDateTimeEdit, QMessageBox
from PyQt5.QtCore import QDateTime
from banco_de_dados import Material, session, Fornecedor


class TelaRegistroMaterial(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Formulário de Material')
        self.resize(400, 200)  # Ajusta o tamanho para o mesmo do exemplo

        # Layout
        layout = QFormLayout()

        # Widgets
        self.nome_input = QLineEdit()
        self.nome_input.setFixedWidth(300)  # Define a largura fixa para o campo de nome

        self.preco_input = QDoubleSpinBox()
        self.preco_input.setFixedWidth(150)  # Define a largura fixa para o campo de preço
        self.preco_input.setDecimals(2)  # Define o número de casas decimais
        self.preco_input.setMinimum(0.0)  # Define o valor mínimo
        self.preco_input.setMaximum(1e6)  # Define o valor máximo, ajuste conforme necessário

        self.nota_fiscal_input = QLineEdit()
        self.nota_fiscal_input.setFixedWidth(150)  # Define a largura fixa para o campo de nota fiscal

        self.quantidade_input = QSpinBox()
        self.quantidade_input.setFixedWidth(100)  # Define a largura fixa para o campo de quantidade
        self.quantidade_input.setMinimum(0)  # Define o valor mínimo
        self.quantidade_input.setMaximum(1e6)  # Define o valor máximo, ajuste conforme necessário

        self.patrimonio_input = QLineEdit()
        self.patrimonio_input.setFixedWidth(150)  # Define a largura fixa para o campo de patrimônio

        self.fornecedor_input = QLineEdit()
        self.fornecedor_input.setFixedWidth(300)  # Define a largura fixa para o campo de fornecedor

        self.data_input = QDateTimeEdit()
        self.data_input.setFixedWidth(150)
        self.data_input.setDateTime(QDateTime.currentDateTime())  # Define a data e hora atual como padrão

        # Adicionar widgets ao layout
        layout.addRow(QLabel('Nome:'), self.nome_input)
        layout.addRow(QLabel('Preço:'), self.preco_input)
        layout.addRow(QLabel('Nota Fiscal:'), self.nota_fiscal_input)
        layout.addRow(QLabel('Quantidade:'), self.quantidade_input)
        layout.addRow(QLabel('Patrimônio:'), self.patrimonio_input)
        layout.addRow(QLabel('Fornecedor:'), self.fornecedor_input)
        layout.addRow(QLabel('Data:'), self.data_input)

        # Botão de Salvar
        self.save_button = QPushButton('Salvar')
        self.save_button.setFixedSize(100, 30)
        self.save_button.clicked.connect(self.salvar_material)
        layout.addWidget(self.save_button)

        # Aplicar layout
        self.setLayout(layout)

        # Estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff; /* Cor de fundo azul claro */
            }
            QLabel {
                color: #003366; /* Cor do texto das labels */
                font-weight: bold;
                font-size: 14px; /* Tamanho da fonte das labels */
            }
            QLineEdit, QDoubleSpinBox, QSpinBox, QDateTimeEdit {
                border: 1px solid #003366; /* Borda azul */
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff; /* Cor de fundo branco para campos de entrada */
            }
            QPushButton {
                background-color: #003366; /* Cor de fundo azul escuro para botões */
                color: #ffffff; /* Cor do texto dos botões */
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00509e; /* Cor de fundo azul claro ao passar o mouse */
            }
        """)

    def salvar_material(self):
        nome = self.nome_input.text()
        preco = self.preco_input.value()
        nota_fiscal = self.nota_fiscal_input.text()
        quantidade = self.quantidade_input.value()
        patrimonio = self.patrimonio_input.text()
        fornecedor_nome = self.fornecedor_input.text()
        data = self.data_input.dateTime().toPyDateTime()

        if not nome:
            QMessageBox.warning(self, 'Erro', 'O nome do material não pode ser nulo!')
            return

        try:
            if patrimonio:  # Verifica se o patrimônio não é nulo
                material_existente = session.query(Material).filter_by(patrimonio=patrimonio).first()
                if material_existente:
                    QMessageBox.warning(self, 'Erro', 'Patrimônio já existe!')
                    return

            if nota_fiscal:
                material_existente = session.query(Material).filter_by(nota_fiscal=nota_fiscal).first()
                if material_existente:
                    QMessageBox.warning(self, 'Erro', 'Nota Fiscal já existe!')
                    return

            # Verifique se o fornecedor já está cadastrado
            fornecedor_existente = session.query(Fornecedor).filter_by(nome=fornecedor_nome).first()
            if not fornecedor_existente:
                # Se o fornecedor não estiver cadastrado, crie um novo registro
                fornecedor_existente = Fornecedor(nome=fornecedor_nome, cnpj='')
                session.add(fornecedor_existente)
                session.commit()

            # Crie um novo material
            new_material = Material(
                nome=nome,
                preco=preco,
                nota_fiscal=nota_fiscal,
                quantidade=quantidade,
                patrimonio=patrimonio,
                data=data
            )

            session.add(new_material)
            session.commit()

            self.mostrar_mensagem_sucesso()
            self.clear_inputs()

        except Exception as e:
            # Em caso de erro, exiba uma mensagem de erro
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao registrar o material: {str(e)}')

    def mostrar_mensagem_sucesso(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Material registrado com sucesso!")
        msg.setWindowTitle("Sucesso")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear_inputs(self):
        self.nome_input.clear()
        self.preco_input.clear()
        self.nota_fiscal_input.clear()
        self.quantidade_input.clear()
        self.patrimonio_input.clear()
        self.fornecedor_input.clear()
        self.data_input.setDateTime(QDateTime.currentDateTime())  # Reseta a data e hora para o valor atual
