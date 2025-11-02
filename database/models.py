from sqlalchemy import String, Date, Float, ForeignKey, Enum, create_engine
from sqlalchemy.orm  import DeclarativeBase, mapped_column, Mapped, relationship, Session
from datetime import date
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

class Usuarios(UserMixin, Base):
    __tablename__ = 'Usuarios'
    id:Mapped[int] = mapped_column("ID_usuario", primary_key=True, autoincrement=True)
    Nome_usuario:Mapped[str] = mapped_column(String(255),nullable=False)
    Email:Mapped[str] = mapped_column(String(255), nullable=False)
    Numero_telefone:Mapped[str] = mapped_column(String(15), nullable=False)
    Data_inscricao:Mapped[date] = mapped_column(Date(), nullable=False)
    Multa_atual:Mapped[float] = mapped_column(nullable=False)
    
    def get_id(self):
        return str(self.id)

