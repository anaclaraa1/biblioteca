from flask import render_template, url_for, request,redirect, Blueprint, flash
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine
editora = Blueprint('editora', __name__, template_folder='../templates')

@editora.route('/register_editoras', methods=['GET', 'POST'])
def register_editoras():
    if request.method == 'POST':
        nome_editora = request.form.get('nome_editora')
        endereco = request.form.get('endereco')
        with Session(bind=engine) as db:
            resultado = db.execute(text("SELECT * FROM Editoras WHERE Nome_editora = :nome"), {"nome": nome_editora})
            resultado = resultado.fetchall()
            if not resultado:       
                db.execute(
                    text("""
                            INSERT INTO Editoras
                                (Nome_editora, Endereco_editora)
                            VALUES 
                                (:editora, :endereco)
                        """),
                        {
                            "editora": nome_editora,
                            "endereco": endereco
                        }
                )
                db.commit()
                flash('Editora cadastrada com sucesso!', category='success')
                return redirect(url_for('index'))
            flash('Esta editora já está cadastrada no sistema.!', category='error')
    return render_template('editora/register_editora.html')