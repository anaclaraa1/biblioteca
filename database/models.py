from sqlalchemy import String, Date, Float, ForeignKey, Enum, create_engine
from sqlalchemy.orm  import DeclarativeBase, mapped_column, Mapped, relationship, Session
from datetime import date
from flask_login import UserMixin

engine = create_engine('mysql://root@localhost:3306/db_biblioteca_2M')
session = Session(bind=engine)


class Base(DeclarativeBase):
    pass

class Usuarios(UserMixin, Base):
    __tablename__ = 'Usuarios'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nome_usuario:Mapped[str] = mapped_column(String(255),nullable=False)
    Email:Mapped[str] = mapped_column(String(255), nullable=False)
    Numero_telefone:Mapped[str] = mapped_column(String(15), nullable=False)
    Data_incricao:Mapped[date] = mapped_column(Date(), nullable=False)
    Multa_atual:Mapped[float] = mapped_column(nullable=False)

    Emprestimos = relationship("Emprestimo", backref="usuario")
    
    def get_id(self):
        return str(self.id)
    
class Livro(Base):
    __tablename__ = 'Livros'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Titulo:Mapped[str] = mapped_column(String(255),nullable=False)
    ISBN:Mapped[str] = mapped_column(String(13),nullable=False)
    Ano_publicacao:Mapped[int] = mapped_column(nullable=False)
    Quantidade_disponivel:Mapped[int] = mapped_column(nullable=False)
    Resumo:Mapped[str] = mapped_column(String(),nullable=False)

    Autor_id:Mapped[int] = mapped_column(ForeignKey('Autores.id'),nullable=False)
    Genero_id:Mapped[int] = mapped_column(ForeignKey('Generos.id'),nullable=False)
    Editora_id:Mapped[int] = mapped_column(ForeignKey('Editoras.id'),nullable=False)

    Emprestimos = relationship("Emprestimo", backref="livro")
    
class Editora(Base):
    __tablename__ = 'Editoras'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nome_editora:Mapped[str] = mapped_column(String(255),nullable=False)
    Endereco_editora:Mapped[str] = mapped_column(nullable=False)

    Livros = relationship('Livro', backref='editora')

class Genero(Base):
    __tablename__ = 'Generos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nome_genero:Mapped[str] = mapped_column(String(255),nullable=False)

    Livros = relationship('Livro', backref='genero')

class Autor(Base):
    __tablename__ = 'Autores'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Nome_autor:Mapped[str] = mapped_column(String(255),nullable=False)
    Nacionalidade:Mapped[str] = mapped_column(String(255),nullable=False)
    Data_nascimento:Mapped[date] = mapped_column(Date(), nullable=False)
    Biografia:Mapped[str] = mapped_column()

    Livros = relationship('Livro', backref='autor')

class Emprestimo(Base):
    __tablename__ = 'Emprestimos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Data_emprestimo:Mapped[date] = mapped_column(Date(), nullable=False)
    Data_devolucao_prevista:Mapped[date] = mapped_column(Date(), nullable=False)
    Data_devolucao_real:Mapped[date] = mapped_column(Date(), nullable=False)
    status_emprestimo: Mapped[str] = mapped_column(Enum('pendente', 'devolvido', 'atrasado', name='status_emprestimo_enum'), nullable=False)

    Usuario_id:Mapped[int] = mapped_column(ForeignKey('Usuarios.id'),nullable=False)
    Livro_id:Mapped[int] = mapped_column(ForeignKey('Livros.id'),nullable=False)