from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
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
    preco = Column(Float, nullable=False)
    nota_fiscal = Column(String, nullable=True)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    patrimonio = Column(String, nullable=True)
    valor_minimo = Column(Float)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))  # Chave estrangeira para Fornecedor


    fornecedor = relationship('Fornecedor')
    # Relacionamento com RetiradaMaterial
    retiradas = relationship("RetiradaMaterial", back_populates="material")

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String)

class Tecnico(Base):
    __tablename__ = 'tecnicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False)

class RetiradaMaterial(Base):
    __tablename__ = 'retiradas'

    id = Column(Integer, primary_key=True)
    ordem_servico = Column(String, unique=True, nullable=False)
    nome_produto = Column(String, nullable=False)
    tecnico_nome = Column(String, nullable=False)
    quantidade = Column(String, nullable=False)
    data_retirada = Column(DateTime, default=datetime.utcnow)
    local_utilizacao = Column(String, nullable=False)
    patrimonio = Column(String, nullable=False)
    retornado = Column(Boolean, default=False)

    # Chave estrangeira para referenciar a tabela Material
    material_id = Column(Integer, ForeignKey('materiais.id'), nullable=False)
    material = relationship("Material", back_populates="retiradas")

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
