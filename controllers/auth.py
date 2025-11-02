from flask import render_template, url_for, request, redirect, Blueprint
from sqlalchemy.orm import Session
from database import engine
from flask_login import login_user, login_required, logout_user
from database.models import Usuarios
from datetime import date


auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('tel')
        data_atual = date.today()
        with Session(bind=engine) as db:
            user_exist = db.query(Usuarios).where(Usuarios.Email == email).first()
            if not user_exist:
                user_novo = Usuarios(Nome_usuario=nome, Email=email, Data_inscricao=data_atual, Numero_telefone=telefone, Multa_atual=0)
                db.add(user_novo)
                db.commit()
                login_user(user_novo)
                return redirect(url_for('index'))
            #f
    return render_template('user/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        with Session(bind=engine) as db:
            user_exist = db.query(Usuarios).where(Usuarios.Email == email).first()
        if user_exist:
            login_user(user_exist)
            return redirect(url_for('index'))
        #f
    return render_template('user/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))