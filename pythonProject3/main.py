from PyQt5 import QtWidgets
from telas.tela_login import TelaLogin
from telas.tela_cadastro import TelaCadastro
from telas.tela_mostrar_usuario import TelaMostrarUsuarios
from telas.tela_registro_fornecedor import TelaRegistroFornecedor
from telas.tela_registro_material import TelaRegistroMaterial
from telas.tela_mostrar_material_registrado import TelaMostrarMateriais
from imagens.imagem import ImageWidget
from telas.tela_registro_tecnico import TelaRegistroTecnico
from telas.tela_retirar_material import TelaRetirarMaterial
from telas.tela_retorno_material import TelaRetornoMaterial
from telas.tela_mostrar_material_retirado import TelaMateriaisRetirados
from telas.tela_estoque_total import TelaEstoque
from telas.tela_procurar_pdf import TelaProcurarPDF  # Importe a nova tela
from telas.tela_mostrar_tecnico import TelaMostrarTecnicos
from telas.tela_mostrar_fornecedor import TelaFornecedores


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, authenticated_user):
        super().__init__()
        self.authenticated_user = authenticated_user
        self.setWindowTitle('Aplicação')
        self.init_ui()

    def init_ui(self):
        # Criação da barra de menu
        menubar = self.menuBar()

        # Criação dos menus
        usuario_menu = menubar.addMenu('Usuário')
        material_menu = menubar.addMenu('Material')
        fornecedor_menu = menubar.addMenu('Fornecedor')
        tecnico_menu = menubar.addMenu('Técnico')
        pdf_menu = menubar.addMenu('PDFs')

        # Criação das ações do menu Usuário
        cadastro_action = QtWidgets.QAction('Cadastro', self)
        if self.authenticated_user == 'admin':
            cadastro_action.triggered.connect(self.abrir_cadastro)
        else:
            cadastro_action.setEnabled(False)
        mostrar_usuarios_action = QtWidgets.QAction('Mostrar Usuários', self)
        mostrar_usuarios_action.triggered.connect(self.abrir_mostrar_usuarios)

        logout_action = QtWidgets.QAction('Logout', self)  # Adicionando a ação de logout
        logout_action.triggered.connect(self.logout)

        # Adição das ações ao menu Usuário
        usuario_menu.addAction(cadastro_action)
        usuario_menu.addAction(mostrar_usuarios_action)
        usuario_menu.addSeparator()  # Separador para organizar o menu
        usuario_menu.addAction(logout_action)  # Adicionar o botão de logout

        # Criação das ações do menu Material
        registrar_material_action = QtWidgets.QAction('Registrar Material', self)
        registrar_material_action.triggered.connect(self.registrar_material)
        mostrar_materiais_action = QtWidgets.QAction('Mostrar Materiais', self)
        mostrar_materiais_action.triggered.connect(self.abrir_mostrar_materiais)
        retirar_material_action = QtWidgets.QAction('Retirar Material', self)
        retirar_material_action.triggered.connect(self.abrir_retirar_material)
        retorno_material_action = QtWidgets.QAction('Retornar Material', self)
        retorno_material_action.triggered.connect(self.abrir_retorno_material)
        materiais_retirados_action = QtWidgets.QAction('Materiais Retirados', self)
        materiais_retirados_action.triggered.connect(self.abrir_materiais_retirados)
        estoque_action = QtWidgets.QAction('Estoque Total', self)
        estoque_action.triggered.connect(self.abrir_estoque)

        # Adição das ações ao menu Material
        material_menu.addAction(registrar_material_action)
        material_menu.addAction(mostrar_materiais_action)
        material_menu.addAction(retirar_material_action)
        material_menu.addAction(retorno_material_action)
        material_menu.addAction(materiais_retirados_action)
        material_menu.addAction(estoque_action)

        # Criação das ações do menu Fornecedor
        registro_fornecedor_action = QtWidgets.QAction('Cadastro de Fornecedor', self)
        registro_fornecedor_action.triggered.connect(self.abrir_registro_fornecedor)
        fornecedor_menu.addAction(registro_fornecedor_action)

        mostrar_fornecedores_action = QtWidgets.QAction('Mostrar Fornecedores', self)
        mostrar_fornecedores_action.triggered.connect(self.abrir_mostrar_fornecedores)
        fornecedor_menu.addAction(mostrar_fornecedores_action)

        # Criação das ações do menu Técnico
        registro_tecnico_action = QtWidgets.QAction('Cadastro de Técnico', self)
        registro_tecnico_action.triggered.connect(self.abrir_registro_tecnico)
        tecnico_menu.addAction(registro_tecnico_action)

        mostrar_tecnico_action = QtWidgets.QAction('Mostrar Técnico', self)
        mostrar_tecnico_action.triggered.connect(self.abrir_mostrar_tecnico)
        tecnico_menu.addAction(mostrar_tecnico_action)

        # Criação das ações do menu PDFs
        procurar_pdfs_action = QtWidgets.QAction('Procurar PDFs', self)
        procurar_pdfs_action.triggered.connect(self.abrir_procurar_pdfs)

        # Adição das ações ao menu PDFs
        pdf_menu.addAction(procurar_pdfs_action)

        # Adicionar imagem de fundo
        self.image_widget = ImageWidget('C:/Users/Detel/Desktop/logo-pjerj-preto.png')
        self.setCentralWidget(self.image_widget)

    def abrir_cadastro(self):
        self.tela_cadastro = TelaCadastro()
        self.tela_cadastro.show()

    def abrir_mostrar_usuarios(self):
        self.tela_mostrar_usuarios = TelaMostrarUsuarios()
        self.tela_mostrar_usuarios.show()

    def registrar_material(self):
        try:
            self.tela_registro_material = TelaRegistroMaterial()
            self.tela_registro_material.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro',
                                           f'Ocorreu um erro ao abrir a tela de registro de material: {e}')

    def abrir_mostrar_materiais(self):
        self.tela_mostrar_materiais = TelaMostrarMateriais()
        self.tela_mostrar_materiais.show()

    def abrir_registro_fornecedor(self):
        self.tela_registro_fornecedor = TelaRegistroFornecedor()
        self.tela_registro_fornecedor.show()

    def abrir_registro_tecnico(self):
        self.tela_registro_tecnico = TelaRegistroTecnico()
        self.tela_registro_tecnico.show()

    def abrir_mostrar_tecnico(self):
        self.tela_mostrar_tecnico = TelaMostrarTecnicos()
        self.tela_mostrar_tecnico.show()

    def abrir_retirar_material(self):
        self.tela_retirar_material = TelaRetirarMaterial()
        self.tela_retirar_material.show()

    def abrir_retorno_material(self):
        self.tela_retorno_material = TelaRetornoMaterial()
        self.tela_retorno_material.show()

    def abrir_materiais_retirados(self):
        self.tela_materiais_retirados = TelaMateriaisRetirados()
        self.tela_materiais_retirados.show()

    def abrir_estoque(self):
        try:
            self.tela_estoque = TelaEstoque()
            self.tela_estoque.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Erro', f'Não foi possível abrir a tela de estoque: {e}')

    def abrir_procurar_pdfs(self):
        self.tela_procurar_pdfs = TelaProcurarPDF()
        self.tela_procurar_pdfs.show()

    def abrir_mostrar_fornecedores(self):
        self.tela_mostrar_fornecedores = TelaFornecedores()
        self.tela_mostrar_fornecedores.show()

    def logout(self):
        # Confirmação de logout
        reply = QtWidgets.QMessageBox.question(
            self, 'Logout', 'Tem certeza de que deseja sair?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.hide()  # Esconde a aplicação principal

            self.tela_login = TelaLogin()
            if self.tela_login.exec_():
                # Se o login for bem-sucedido, reabrir a aplicação principal
                self.authenticated_user = self.tela_login.username_input.text()
                self.show()  # Reexibe a aplicação principal

    def closeEvent(self, event):
        # Confirmação ao fechar a aplicação
        reply = QtWidgets.QMessageBox.question(
            self, 'Fechar', 'Tem certeza de que deseja sair?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()  # Aceita o fechamento
        else:
            event.ignore()  # Ignora o fechamento

    def show_full_screen_excluding_taskbar(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()  # Obtém o retângulo da tela excluindo a área da barra de tarefas
        self.setGeometry(screen_rect)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    # Exibir tela de login primeiro
    tela_login = TelaLogin()
    if tela_login.exec_():
        # Se o login for bem-sucedido, exibir a aplicação principal
        main_app = MainApp(tela_login.username_input.text())
        main_app.show_full_screen_excluding_taskbar()  # Abre a aplicação em tela cheia excluindo a barra de tarefas
        app.exec_()
    else:
        # Se o login falhar, sair do aplicativo
        app.quit()