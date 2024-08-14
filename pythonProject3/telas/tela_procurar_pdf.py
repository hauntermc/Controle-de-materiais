import os
import subprocess
import sys
from PyQt5 import QtWidgets, QtGui

class TelaProcurarPDF(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Procurar PDFs Gerados')
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Campo de pesquisa por nome
        self.pesquisa_input = QtWidgets.QLineEdit()
        self.pesquisa_input.setPlaceholderText('Digite o nome do PDF para buscar')

        # Adicionar uma lista para exibir os PDFs encontrados
        self.lista_pdfs = QtWidgets.QListWidget()

        # Adicionar botões
        procurar_button = QtWidgets.QPushButton('Procurar PDFs')
        abrir_button = QtWidgets.QPushButton('Abrir PDF Selecionado')
        pesquisar_button = QtWidgets.QPushButton('Pesquisar')

        procurar_button.clicked.connect(self.procurar_pdfs)
        abrir_button.clicked.connect(self.abrir_pdf_selecionado)
        pesquisar_button.clicked.connect(self.pesquisar_pdf)

        layout.addWidget(self.pesquisa_input)
        layout.addWidget(pesquisar_button)
        layout.addWidget(self.lista_pdfs)
        layout.addWidget(procurar_button)
        layout.addWidget(abrir_button)

        self.setLayout(layout)

    def procurar_pdfs(self):
        # Abrir uma janela de diálogo para selecionar uma pasta
        pasta = QtWidgets.QFileDialog.getExistingDirectory(self, "Selecione a pasta onde os PDFs estão salvos")
        if pasta:
            self.lista_pdfs.clear()
            self.pasta_selecionada = pasta  # Guardar a pasta selecionada
            self.pdf_map = {}  # Mapeia nomes de PDFs para seus caminhos completos
            for root, _, files in os.walk(pasta):
                for file in files:
                    if file.endswith('.pdf'):
                        nome_arquivo = os.path.basename(file)
                        self.lista_pdfs.addItem(nome_arquivo)
                        self.pdf_map[nome_arquivo] = os.path.join(root, file)

    def pesquisar_pdf(self):
        # Filtrar a lista de PDFs com base no nome inserido
        filtro = self.pesquisa_input.text().lower()
        self.lista_pdfs.clear()
        if hasattr(self, 'pasta_selecionada') and self.pasta_selecionada:
            for nome_arquivo, caminho_arquivo in self.pdf_map.items():
                if filtro in nome_arquivo.lower():
                    self.lista_pdfs.addItem(nome_arquivo)
                    self.pdf_map[nome_arquivo] = caminho_arquivo  # Atualizar o mapa com o caminho completo

    def abrir_pdf_selecionado(self):
        item_selecionado = self.lista_pdfs.currentItem()
        if item_selecionado:
            pdf_nome = item_selecionado.text()
            if pdf_nome in self.pdf_map:
                pdf_filename = self.pdf_map[pdf_nome]
                self.abrir_pdf(pdf_filename)

    def abrir_pdf(self, pdf_filename):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_filename)
            elif os.name == 'posix':  # macOS ou Linux
                subprocess.run(['open', pdf_filename] if sys.platform == 'darwin' else ['xdg-open', pdf_filename])
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Não foi possível abrir o PDF: {str(e)}')
