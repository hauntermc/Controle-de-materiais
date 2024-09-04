from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import bcrypt

# Configuração da base
Base = declarative_base()

# Definição da tabela Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

class Material(Base):
    __tablename__ = 'materiais'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    tipo = Column(String, nullable=False)  # 'Bem de Consumo' ou 'Bem Permanente'
    codigo = Column(String, nullable=False)  # RM ou NF

    estoques = relationship("Estoque", back_populates="material")
    requisicoes = relationship("Requisicao", back_populates="produto")

    def __repr__(self):
        return f"<Material(nome={self.nome}, tipo={self.tipo}, codigo={self.codigo})>"

class Estoque(Base):
    __tablename__ = 'estoques'

    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    valor_minimo = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # Pode ser 'Urgente', 'Alerta', 'Normal'

    material_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    material = relationship("Material", back_populates="estoques")


class EntradaProduto(Base):
    __tablename__ = 'entradas_produtos'

    id = Column(Integer, primary_key=True)
    tipo_documento = Column(String, nullable=False)
    numero_documento = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    produto = relationship('Material')
    quantidade = Column(Float, nullable=False)
    data_entrada = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        produto_nome = self.produto.nome if self.produto else "Produto não encontrado"
        return f"<EntradaProduto(tipo_documento={self.tipo_documento}, numero_documento={self.numero_documento}, produto={produto_nome}, data_entrada={self.data_entrada})>"


class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String)
    email = Column(String)

class Tecnico(Base):
    __tablename__ = 'tecnicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)

class Requisicao(Base):
    __tablename__ = 'requisicoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    produto_nome = Column(String, nullable=False)
    matricula_tecnico = Column(String, ForeignKey('tecnicos.matricula'), nullable=False)
    nome_tecnico = Column(String)
    quantidade = Column(Float, nullable=False)
    data_requisicao = Column(DateTime, nullable=False)
    nome_usuario = Column(String, ForeignKey('usuarios.username'), nullable=False)
    local_retirada = Column(String)
    status = Column(String, default='Aberta')
    numero_nf = Column(String)  # Novo campo
    numero_sm = Column(String)  # Novo campo

    produto = relationship("Material", back_populates="requisicoes")
    tecnico = relationship("Tecnico", foreign_keys=[matricula_tecnico])
    usuario = relationship("Usuario", foreign_keys=[nome_usuario])

    def __repr__(self):
        return (f"<Requisicao(ordem_servico={self.ordem_servico}, produto_nome={self.produto_nome}, "
                f"matricula_tecnico={self.matricula_tecnico}, nome_tecnico={self.nome_tecnico}, "
                f"quantidade={self.quantidade}, data_requisicao={self.data_requisicao}, "
                f"nome_usuario={self.nome_usuario}, status={self.status}, "
                f"numero_nf={self.numero_nf}, numero_sm={self.numero_sm})>")



class Devolucao(Base):
    __tablename__ = 'devolucoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_servico = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    produto_nome = Column(String, nullable=False)
    quantidade = Column(Float, nullable=False)
    data_devolucao = Column(DateTime, default=datetime.utcnow, nullable=False)
    motivo_retorno = Column(String)
    numero_nf = Column(String)  # Novo campo
    numero_sm = Column(String)  # Novo campo

    produto = relationship("Material")

    def __repr__(self):
        return (f"<Devolucao(ordem_servico={self.ordem_servico}, produto_nome={self.produto_nome}, "
                f"quantidade={self.quantidade}, data_devolucao={self.data_devolucao}, "
                f"motivo_retorno={self.motivo_retorno}, numero_nf={self.numero_nf}, "
                f"numero_sm={self.numero_sm})>")

# Configuração do banco de dados (usando SQLite neste exemplo)
DATABASE_URL = 'sqlite:///materiais.db'
engine = create_engine(DATABASE_URL, echo=True)

# Criação das tabelas
Base.metadata.create_all(engine)

# Configuração da sessão
Session = sessionmaker(bind=engine)
session = Session()

# Função para criar o usuário "admin" se ele ainda não existir
def create_admin_user():
    # Verificar se o usuário "admin" já existe
    admin_user = session.query(Usuario).filter_by(username='admin').first()

    if not admin_user:
        # Gerar um hash para a senha "admin"
        hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())

        # Criar o usuário "admin"
        admin_user = Usuario(nome='Administrador', username='admin', senha=hashed_password.decode('utf-8'))
        session.add(admin_user)
        session.commit()
        print("Usuário 'admin' criado com sucesso.")
    else:
        print("Usuário 'admin' já existe.")

# Chame essa função quando inicializar sua aplicação
create_admin_user()