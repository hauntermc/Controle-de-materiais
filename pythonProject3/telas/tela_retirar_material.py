import os
import subprocess
import sys
from datetime import datetime
from PyQt5 import QtWidgets
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from banco_de_dados import session, Material, RetiradaMaterial, Tecnico
  # Certifique-se de que esta variável está definida


class TelaRetirarMaterial(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Retirar Material')
        self.setGeometry(100, 100, 500, 500)  # Aumentar a altura para acomodar o novo campo
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Estilizar a janela com uma cor de fundo azul clara e cantos arredondados
        self.setStyleSheet("""
                   QWidget {
                       background-color: #f0f8ff; /* Cor de fundo azul claro */
                       border-radius: 10px;
                       font-family: Arial, sans-serif;
                   }
                   QLabel {
                       color: #003366;
                       font-weight: bold;
                       font-size: 12pt;
                       margin-bottom: 5px;
                   }
                   QLineEdit, QComboBox {
                       background-color: #ffffff;
                       border: 2px solid #003366;
                       padding: 8px;
                       border-radius: 5px;
                       font-size: 10pt;
                   }
                   QPushButton {
                       background-color: #003366;
                       color: white;
                       font-weight: bold;
                       border-radius: 5px;
                       padding: 10px;
                       font-size: 10pt;
                   }
                   QPushButton:hover {
                       background-color: #0055a5;
                   }
               """)

        # Adicionar campos de entrada
        self.ordem_servico_input = QtWidgets.QLineEdit()
        self.ordem_servico_input.setFixedWidth(200)
        self.nome_produto_input = QtWidgets.QComboBox()
        self.quantidade_input = QtWidgets.QLineEdit()
        self.quantidade_input.setFixedWidth(100)
        self.tecnico_nome_input = QtWidgets.QLineEdit()
        self.tecnico_nome_input.setFixedWidth(200)
        self.local_utilizacao_input = QtWidgets.QLineEdit()
        self.local_utilizacao_input.setFixedWidth(200)
        self.patrimonio_input = QtWidgets.QLineEdit()
        self.patrimonio_input.setFixedWidth(150)

        # Novo campo para o responsável pela liberação do material
        self.responsavel_lib_input = QtWidgets.QLineEdit()
        self.responsavel_lib_input.setFixedWidth(200)

        # Adicionar botões
        retirar_button = QtWidgets.QPushButton('Retirar')
        retirar_button.clicked.connect(self.retirar_material)

        atualizar_button = QtWidgets.QPushButton('Atualizar')
        atualizar_button.clicked.connect(self.carregar_materiais)

        # Adicionar os widgets ao layout com espaçamento
        layout.addWidget(QtWidgets.QLabel('Ordem de Serviço:'))
        layout.addWidget(self.ordem_servico_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Produto:'))
        layout.addWidget(self.nome_produto_input)
        layout.addWidget(QtWidgets.QLabel('Quantidade:'))
        layout.addWidget(self.quantidade_input)
        layout.addWidget(QtWidgets.QLabel('Nome do Técnico:'))
        layout.addWidget(self.tecnico_nome_input)
        layout.addWidget(QtWidgets.QLabel('Local de Utilização:'))
        layout.addWidget(self.local_utilizacao_input)
        layout.addWidget(QtWidgets.QLabel('Patrimônio:'))
        layout.addWidget(self.patrimonio_input)
        layout.addWidget(QtWidgets.QLabel('Responsável pela Liberação:'))
        layout.addWidget(self.responsavel_lib_input)
        layout.addWidget(retirar_button)
        layout.addWidget(atualizar_button)

        self.setLayout(layout)

    def carregar_materiais(self):
        try:
            materiais = session.query(Material).filter(Material.quantidade > 0).all()
            self.nome_produto_input.clear()
            self.nome_produto_input.addItem("Selecione um material")
            self.material_patrimonios = {}
            for material in materiais:
                self.nome_produto_input.addItem(material.nome)
                self.material_patrimonios[material.nome] = material.patrimonio

            # Atualiza o patrimônio com base na seleção atual
            self.atualizar_patrimonio()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Ocorreu um erro ao carregar os materiais: {str(e)}')

    def atualizar_patrimonio(self):
        nome_produto = self.nome_produto_input.currentText()
        if nome_produto in self.material_patrimonios:
            self.patrimonio_input.setText(str(self.material_patrimonios[nome_produto]))
        else:
            self.patrimonio_input.clear()

    def limpar_campos(self):
        self.ordem_servico_input.clear()
        self.nome_produto_input.clear()
        self.tecnico_nome_input.clear()
        self.local_utilizacao_input.clear()
        self.patrimonio_input.clear()
        self.quantidade_input.clear()

    def retirar_material(self):
        ordem_servico = self.ordem_servico_input.text()
        nome_produto = self.nome_produto_input.currentText()
        tecnico_nome = self.tecnico_nome_input.text()
        local_utilizacao = self.local_utilizacao_input.text()
        patrimonio = self.patrimonio_input.text()
        quantidade = self.quantidade_input.text()
        responsavel_lib = self.responsavel_lib_input.text()  # Novo campo

        if not quantidade.isdigit() or int(quantidade) <= 0:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'A quantidade deve ser um número maior que 0.')
            return

        try:
            self.registrar_retirada(ordem_servico, nome_produto, quantidade, tecnico_nome, local_utilizacao, patrimonio)
            QtWidgets.QMessageBox.information(self, 'Sucesso', 'Material retirado com sucesso!')

            hoje = datetime.now().strftime("%d/%m/%Y")
            material_info = {
                'data_retirada': hoje,
                'nome_tecnico': tecnico_nome,
                'matricula_tecnico': '',
                'responsavel_controle': responsavel_lib,
                'matricula_responsavel': '',
                'local_destino': local_utilizacao,
                'numero_patrimonio': patrimonio,
                'tecnico_responsavel': tecnico_nome,
                'matricula_tecnico_responsavel': '',
                'supervisor_tecnico': '',
                'matricula_supervisor': '',
                'controle_materiais': '',
                'matricula_controle': '',

            }

            pdf_filename = f"{ordem_servico}.pdf"
            generate_form_pdf(pdf_filename, ordem_servico, material_info)

            QtWidgets.QMessageBox.information(self, 'PDF Gerado', f'O PDF foi gerado com sucesso: {pdf_filename}')
            self.abrir_pdf(pdf_filename)

            self.carregar_materiais()
            self.limpar_campos()

        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', str(e))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Ocorreu um erro inesperado: {str(e)}')

    def registrar_retirada(self, ordem_servico, nome_produto, quantidade, tecnico_nome, local_utilizacao, patrimonio):
        try:
            tecnico = session.query(Tecnico).filter_by(nome=tecnico_nome).first()
            if not tecnico:
                raise ValueError("Técnico não registrado no banco de dados.")

            retirada_existente = session.query(RetiradaMaterial).filter_by(ordem_servico=ordem_servico).first()
            if retirada_existente:
                raise ValueError("Já existe uma retirada com essa ordem de serviço.")

            material = session.query(Material).filter_by(nome=nome_produto, patrimonio=patrimonio).first()
            if material is None:
                raise ValueError("Material não encontrado")
            if material.quantidade < int(quantidade):
                raise ValueError("Quantidade solicitada maior que a disponível")

            retirada = RetiradaMaterial(
                ordem_servico=ordem_servico,
                nome_produto=nome_produto,
                quantidade=int(quantidade),
                tecnico_nome=tecnico_nome,
                local_utilizacao=local_utilizacao,
                patrimonio=patrimonio,
                material_id=material.id
            )

            material.quantidade -= int(quantidade)
            session.add(retirada)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

    def abrir_pdf(self, pdf_filename):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_filename)
            elif os.name == 'posix':  # macOS ou Linux
                subprocess.run(['open', pdf_filename] if sys.platform == 'darwin' else ['xdg-open', pdf_filename])
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Não foi possível abrir o PDF: {str(e)}')


def generate_form_pdf(filename, ordem_servico, material_info):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    cabecalho = ParagraphStyle(name='centered', alignment=1, fontSize=12)
    elements.append(Paragraph("Poder Judiciário do Estado do Rio de Janeiro - PJERJ", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Departamento de Segurança Eletrônica e de Telecomunicacoes - DETEL", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Serviço de Controle de Materiais", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("REQUISIÇÃO DE MATERIAIS", styles['Title']))
    elements.append(Spacer(1, 12))

    # Horizontal Table Data
    data = [
        ['Número da OS:', ordem_servico, 'Data de retirada:', material_info.get('data_retirada', '____________________')],
        ['Nome do técnico:', material_info.get('nome_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico', '____________________')],
        ['Resp. Controle:', material_info.get('responsavel_controle', '____________________'), 'Matrícula:', material_info.get('matricula_responsavel', '____________________')],
        ['Local de Destino:', material_info.get('local_destino', '____________________')],
        ['Número de Patrimônio:', material_info.get('numero_patrimonio', '____________________')],
        ['Técnico Responsável:', material_info.get('tecnico_responsavel', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico_responsavel', '____________________')],
        ['Supervisor Técnico:', material_info.get('supervisor_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_supervisor', '____________________')],
        ['Controle de Materiais:', material_info.get('controle_materiais', '____________________'), 'Matrícula:', material_info.get('matricula_controle', '____________________')],
        ['Responsável pela Liberação:', material_info.get('responsavel_lib', '____________________')]
    ]

    table = Table(data, colWidths=[150, 150, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add signature lines
    signature_line = '______________________________________'
    elements.append(Paragraph(f"{signature_line}<br/>Assinatura do Técnico", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"{signature_line}<br/>Assinatura do Supervisor", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"{signature_line}<br/>Assinatura do Controle de Materiais", styles['Normal']))
    elements.append(Spacer(1, 12))

    doc.build(elements)
