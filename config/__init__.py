import os
from dotenv import load_dotenv
from flask_login import LoginManager, login_user
from database import Session, engine
from database.models import Usuarios
from sqlalchemy import text


def config_app(app):
    load_dotenv()
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SECRET_KEY is None:
        raise RuntimeError('SECRET_KEY não foi definida')

    app.secret_key = SECRET_KEY

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with Session(bind=engine) as db:
            user = db.execute(
                text('SELECT * FROM Usuarios WHERE ID_usuario = :id'),
                {'id': user_id}).fetchone()
            user = Usuarios(id=user.ID_usuario,nome=user.Nome_usuario, email=user.Email, tel=user.Numero_telefone, data_inscricao=user.Data_inscricao, multa=user.Multa_atual)
        return user
