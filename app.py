from flask import Flask, render_template
from sqlalchemy.orm import Session
from flask_login import LoginManager
from database.models import Usuarios, Base
from controllers.auth import auth_bp
from controllers.livro import livro
from controllers.genero import genero
from database import engine

app = Flask(__name__)
app.secret_key = 'Esconda-me'

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as db:
        user = db.query(Usuarios).where(Usuarios.id == user_id).first()
    return user
# Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

# app.register_blueprint(products.bp)
app.register_blueprint(auth_bp)
app.register_blueprint(livro)
app.register_blueprint(genero)