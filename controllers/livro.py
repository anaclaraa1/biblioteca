from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import  text
from database import engine


livro = Blueprint('livro', __name__, template_folder='../templates')

@livro.route('/livros', methods=['GET'])
@login_required
def livros():
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM livros LEFT JOIN autores ON autores.ID_autor = livros.Autor_id LEFT JOIN generos ON generos.ID_genero = livros.Genero_id LEFT JOIN editoras ON editoras.ID_editora = livros.Editora_id'))
        livros = data.all()
        
    return render_template('livros/listar_livros.html', livros=livros)


@livro.route('/register_livros', methods=['GET', 'POST'])
@login_required
def register_livros():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        isbn = request.form.get('ISBN')
        autor = request.form.get('autor')
        ano = request.form.get('ano')
        genero = request.form.get('genero')
        editora = request.form.get('editora')
        qnt_disponivel = request.form.get('qnt_disponivel')
        resumo = request.form.get('resumo')
        with Session(bind=engine) as db:
            db.execute(
                text("""
                        INSERT INTO Livros 
                            (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
                        VALUES 
                            (:titulo, :autor_id, :isbn, :ano, :genero_id, :editora_id, :quantidade, :resumo)
                    """),
                    {
                        "titulo": titulo,
                        "autor_id": autor,
                        "isbn": isbn,
                        "ano": ano,
                        "genero_id": genero,
                        "editora_id": editora,
                        "quantidade": qnt_disponivel,
                        "resumo": resumo
                    }
            )
            db.commit()
            flash('Livro cadastrada com sucesso!', category='success')
            return redirect(url_for('index'))
    with Session(bind=engine) as db:
        lista_autores = db.execute(text("SELECT * FROM Autores"))
        lista_generos = db.execute(text("SELECT * FROM Generos"))
        lista_editoras = db.execute(text("SELECT * FROM Editoras"))
    return render_template('livros/register_livros.html', lista_generos=lista_generos, lista_editoras=lista_editoras, lista_autores=lista_autores)

@livro.route('/deletar_livros/<int:livro_id>')
@login_required
def deletar_livros(livro_id: int):
    with engine.begin() as conn:
        try:
            conn.execute(
                text(
                    '''
                        delete from livros where ID_livro = :livro_id
                    '''
                ),
                {'livro_id': livro_id}
            )
            conn.commit()
        except IntegrityError:
            flash('Não é possível deletar o livro', category='error')
        else:
            flash('Livro deletado com sucesso', category='success')
    return redirect(url_for('livro.livros'))