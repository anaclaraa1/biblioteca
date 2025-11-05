from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine


genero = Blueprint('genero', __name__, template_folder='../templates')


@genero.route('/register_generos', methods=['GET', 'POST'])
@login_required
def register_generos():
    if request.method == 'POST':
        nome_genero = request.form.get('nome_genero')
        with Session(bind=engine) as db:
            resultado = db.execute(text("SELECT * FROM Generos WHERE Nome_genero = :nome"), {"nome": nome_genero})
            resultado = resultado.fetchall()
            if not resultado:       
                db.execute(
                    text("""
                            INSERT INTO Generos
                                (Nome_genero)
                            VALUES 
                                (:genero)
                        """),
                        {
                            "genero": nome_genero,
                        }
                )
                db.commit()
                flash('Gênero cadastrado com sucesso!', category='success')
                return redirect(url_for('genero.generos'))
            flash('Este gênero já está cadastrado no sistema.!', category='error')
    return render_template('generos/register_genero.html')


@genero.route('/generos')
@login_required
def generos():
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM generos'))
        generos = data.all()
    return render_template('generos/listar_generos.html', generos=generos)


@genero.route('/editar_genero/<int:genero_id>', methods=['GET', 'POST'])
@login_required
def editar_genero(genero_id: int):
    if request.method == 'POST':
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE generos
                        SET Nome_genero = :Nome_genero
                        WHERE ID_genero = :genero_id
                    '''
                ),
                {**request.form, 'genero_id': genero_id}
            )
            conn.commit()
        flash('Dados alterados com sucesso', category='success')
        return redirect(url_for('genero.generos'))
    
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM generos WHERE ID_genero = :genero_id'), {'genero_id': genero_id})
        genero = data.fetchone()
    return render_template('generos/editar_genero.html', genero=genero)
