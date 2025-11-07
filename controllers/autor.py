from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import engine


autor = Blueprint('autor', __name__, template_folder='../templates')


@autor.route('/register_autores', methods=['GET', 'POST'])
@login_required
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
                flash('Autor cadastrado com sucesso!', category='success')
                return redirect(url_for('autor.autores'))
            flash('Autor já está cadastrado no sistema!', category='error')
    return render_template('autores/register_autor.html')


@autor.route('/autores', methods=['GET'])
@login_required
def autores():
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM autores'))
        autores = data.all()
    return render_template('autores/listar_autores.html', autores=autores)


@autor.route('/editar_autor/<int:autor_id>', methods=['GET', 'POST'])
@login_required
def editar_autor(autor_id: int):
    if request.method == 'POST':
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE autores
                        SET Nome_autor = :Nome_autor,
                        Nacionalidade = :Nacionalidade,
                        Data_nascimento = :Data_nascimento,
                        Biografia = :Biografia
                        WHERE ID_autor = :autor_id
                    '''
                ),
                {**request.form, 'autor_id': autor_id}
            )
            conn.commit()
        flash('Dados do alterados com sucesso!', category='success')
        return redirect(url_for('autor.autores'))
    
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM autores WHERE ID_autor = :autor_id'), {'autor_id': autor_id})
        autor = data.fetchone()
    return render_template('autores/editar_autor.html', autor=autor)

@autor.route('/deletar_autor/<int:autor_id>')
@login_required
def deletar_autor(autor_id: int):
    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    '''
                        delete from autores where ID_autor = :autor_id
                    '''
                ),
                {'autor_id': autor_id}
            )
            conn.commit()
        except IntegrityError:
            flash('Não é possível deletar o autor...', category='error')
        else:
            flash('Autor deletado com sucesso!', category='success')
    return redirect(url_for('autor.autores'))