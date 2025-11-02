from flask import render_template, url_for, request,redirect, Blueprint, flash
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine
autor = Blueprint('autor', __name__, template_folder='../templates')

@autor.route('/register_autores', methods=['GET', 'POST'])
def register_autores():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nacionalidade = request.form.get('nacionalidade')
        biografia = request.form.get('biografia')
        nascimento = request.form.get('nascimento')
        with Session(bind=engine) as db:
            resultado = db.execute(text("SELECT * FROM Autores WHERE Nome_autor = :nome"), {"nome": nome})
            resultado = resultado.fetchall()
            if not resultado: 
                db.execute(
                    text("""
                            INSERT INTO Autores 
                                (Nome_autor, Nacionalidade, Data_nascimento, Biografia)
                            VALUES 
                                (:nome, :nacionalidade, :data_nasc, :biografia)
                        """),
                        {
                            "nome": nome,
                            "nacionalidade": nacionalidade,
                            "data_nasc": nascimento,
                            "biografia": biografia
                        }
                )
                db.commit()
                flash('Autor cadastrada com sucesso!', category='success')
                return redirect(url_for('index'))
            flash('Este autor já está cadastrado no sistema.!', category='error')
    return render_template('autores/register_autor.html')
