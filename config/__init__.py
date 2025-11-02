import os
from dotenv import load_dotenv
from flask_login import LoginManager
from database import Session, engine
from database.models import Usuarios


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
            user = db.query(Usuarios).where(Usuarios.id == user_id).first()
        return user
