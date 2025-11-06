from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import date
from flask_login import UserMixin


class Usuarios(UserMixin):
    def __init__(self, id, nome, email, tel, data_inscricao, multa):
        self.id = id
        self.nome = nome
        self.email = email
        self.tel = tel
        self.data_inscricao = data_inscricao
        self.multa = multa
    
    def get_id(self):
        return str(self.id)

