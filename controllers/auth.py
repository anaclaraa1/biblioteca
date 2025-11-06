from flask import render_template, url_for, request, redirect, Blueprint
from sqlalchemy.orm import Session
from sqlalchemy import text
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
            user_exist = db.execute(
                text('SELECT * FROM Usuarios WHERE Email = :email'),
                {'email': email}).fetchone()
            if not user_exist:
                db.execute(
                    text("""
                            INSERT INTO Usuarios
                                (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
                            VALUES 
                                (:nome, :email, :tel, :data_inscricao, :multa)
                        """),
                        {
                            "nome": nome,
                            "email": email,
                            "tel": telefone,
                            "data_inscricao": data_atual,
                            "multa": 0
                        }
                )
                db.commit()
                user_atual = db.execute(
                text('SELECT * FROM Usuarios WHERE Email = :email'),
                {'email': email}).fetchone()
                user_novo = Usuarios(id= user_atual.ID_usuario, nome=nome, email=email, tel=telefone, data_inscricao=data_atual, multa=0)
                login_user(user_novo)
                return redirect(url_for('index'))
            #f
    return render_template('user/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        with Session(bind=engine) as db:
            user_exist = db.execute(
                text('SELECT * FROM Usuarios WHERE Email = :email'),
                {'email': email}).fetchone()
        if user_exist:
            user_exist = Usuarios(id=user_exist.ID_usuario,nome=user_exist.Nome_usuario, email=user_exist.Email, tel=user_exist.Numero_telefone, data_inscricao=user_exist.Data_inscricao, multa=user_exist.Multa_atual)
            login_user(user_exist)
            return redirect(url_for('index'))
        #f
    return render_template('user/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))