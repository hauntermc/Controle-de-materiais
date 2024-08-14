from PyQt5 import QtWidgets, QtGui, QtCore
from banco_de_dados import session, Material, RetiradaMaterial

class TelaRetornoMaterial(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Retorno de Material')
        self.resize(300, 200)  # Ajusta o tamanho para acomodar o ComboBox
        self.setStyleSheet("background-color: #f0f8ff;")  # Cor de fundo azul claro

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QFormLayout()

        # Adicionar campos de entrada com estilo
        self.ordem_servico_input = self.criar_campo('Ordem de Serviço:')
        self.nome_produto_input = self.criar_combo('Nome do Produto:')
        self.tecnico_nome_input = self.criar_campo('Nome do Técnico:')
        self.quantidade_input = self.criar_campo('Quantidade:')
        self.quantidade_input.setFixedWidth(100)
        self.patrimonio_input = self.criar_campo('Patrimônio:')
        self.patrimonio_input.setFixedWidth(150)

        # Adicionar botão de retorno com estilo
        retornar_button = QtWidgets.QPushButton('Retornar')
        retornar_button.setFixedSize(100, 30)
        retornar_button.setStyleSheet(
            "background-color: #003366; color: white; border: none; border-radius: 5px; padding: 10px; font-weight: bold;")
        retornar_button.clicked.connect(self.retornar_material)

        # Adicionar widgets ao layout
        layout.addRow(QtWidgets.QLabel('Ordem de Serviço:'), self.ordem_servico_input)
        layout.addRow(QtWidgets.QLabel('Nome do Produto:'), self.nome_produto_input)
        layout.addRow(QtWidgets.QLabel('Nome do Técnico:'), self.tecnico_nome_input)
        layout.addRow(QtWidgets.QLabel('Quantidade:'), self.quantidade_input)
        layout.addRow(QtWidgets.QLabel('Patrimônio:'), self.patrimonio_input)
        layout.addRow(retornar_button)

        # Aplicar layout
        self.setLayout(layout)

        # Estilo
        self.setStyleSheet("""
            QLabel {
                color: #003366; /* Cor do texto das labels */
                font-weight: bold;
                font-size: 14px; /* Tamanho da fonte das labels */
            }
            QLineEdit {
                border: 1px solid #003366; /* Borda azul */
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff; /* Cor de fundo branco para campos de entrada */
                width: 300px; /* Largura fixa para campos de entrada */
            }
            QComboBox {
                border: 1px solid #003366; /* Borda azul */
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff; /* Cor de fundo branco para o ComboBox */
                width: 300px; /* Largura fixa para o ComboBox */
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

        # Carregar os materiais disponíveis para retorno
        self.carregar_materiais()

    def criar_campo(self, label_text):
        """ Cria um campo de entrada com o rótulo associado e estilo. """
        widget = QtWidgets.QLineEdit()
        widget.setStyleSheet("border: 1px solid #003366; border-radius: 5px; padding: 5px; background-color: #ffffff;")
        widget.setFixedWidth(300)  # Define a largura fixa para o campo de entrada
        return widget

    def criar_combo(self, label_text):
        """ Cria um ComboBox com o rótulo associado e estilo. """
        widget = QtWidgets.QComboBox()
        widget.setStyleSheet("border: 1px solid #003366; border-radius: 5px; padding: 5px; background-color: #ffffff;")
        widget.setFixedWidth(300)  # Define a largura fixa para o ComboBox
        return widget

    def carregar_materiais(self):
        try:
            # Consultar os materiais que podem ser retornados (aqueles que foram retirados e ainda não retornados)
            materiais = session.query(RetiradaMaterial).filter(
                RetiradaMaterial.quantidade > 0,
                RetiradaMaterial.retornado == False  # Adicionar este filtro
            ).all()
            self.nome_produto_input.clear()  # Limpa o ComboBox antes de adicionar novos itens
            self.nome_produto_input.addItem("Selecione um material")
            for retirada in materiais:
                self.nome_produto_input.addItem(f"{retirada.nome_produto} ({retirada.patrimonio})")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Ocorreu um erro ao carregar os materiais: {str(e)}')

    def retornar_material(self):
        ordem_servico = self.ordem_servico_input.text()
        nome_produto = self.nome_produto_input.currentText()
        tecnico_nome = self.tecnico_nome_input.text()
        patrimonio = self.patrimonio_input.text()
        quantidade = self.quantidade_input.text()

        if not nome_produto.startswith("Selecione"):
            nome_produto = nome_produto.split(' (')[0]

        try:
            self.registrar_retorno(ordem_servico, nome_produto, tecnico_nome, quantidade, patrimonio)
            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Material retornado com sucesso!')
            # Atualizar a lista de materiais no ComboBox após o retorno
            self.carregar_materiais()
            # Limpar os campos
            self.limpar_campos()
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', str(e))

    def registrar_retorno(self, ordem_servico, nome_produto, tecnico_nome, quantidade, patrimonio):
        # Verifique se o material está registrado como retirado
        retirada = session.query(RetiradaMaterial).filter_by(
            ordem_servico=ordem_servico,
            nome_produto=nome_produto,
            tecnico_nome=tecnico_nome,
            patrimonio=patrimonio
        ).first()

        if retirada is None:
            raise ValueError("Retirada não encontrada")

        # Recupere o material
        material = session.query(Material).filter_by(nome=nome_produto, patrimonio=patrimonio).first()
        if material is None:
            raise ValueError("Material não encontrado")

        # Interpretar a quantidade
        if quantidade.startswith('DIS'):
            # Lógica para tratar quantidades no formato DIS
            if material.quantidade_textual:
                # Atualize a quantidade textual existente
                material.quantidade_textual = quantidade
            else:
                # Defina a quantidade textual se não existir
                material.quantidade_textual = quantidade
        else:
            try:
                quantidade_int = int(quantidade)  # Verifique se a quantidade é um número válido
                material.quantidade += quantidade_int
            except ValueError:
                raise ValueError("Quantidade deve ser um número inteiro")

        # Marcar como retornado em vez de deletar
        retirada.retornado = True
        session.commit()

    def limpar_campos(self):
        """ Limpa todos os campos de entrada e o ComboBox. """
        self.ordem_servico_input.clear()
        self.nome_produto_input.setCurrentIndex(0)  # Reseta o ComboBox para a primeira opção
        self.tecnico_nome_input.clear()
        self.quantidade_input.clear()
        self.patrimonio_input.clear()
