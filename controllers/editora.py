from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine


editora = Blueprint('editora', __name__, template_folder='../templates')


@editora.route('/register_editoras', methods=['GET', 'POST'])
@login_required
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


@editora.route('/editoras')
@login_required
def editoras():
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM editoras'))
        editoras = data.all()
    return render_template('editora/listar_editoras.html', editoras=editoras)


@editora.route('/editar_editoras/<int:editora_id>', methods=['GET', 'POST'])
@login_required
def editar_editora(editora_id: int):
    if request.method == 'POST':
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE editoras
                        SET Nome_editora = :Nome_editora,
                        Endereco_editora = :Endereco_editora
                        WHERE ID_editora = :editora_id
                    '''
                ),
                {**request.form, 'editora_id': editora_id}
            )
            conn.commit()
        return redirect(url_for('editora.editoras'))
    
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM editoras WHERE ID_editora = :editora_id'), {'editora_id': editora_id})
        editora = data.fetchone()
    return render_template('editora/editar_editora.html', editora=editora)
