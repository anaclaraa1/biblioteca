from flask import render_template, url_for, request,redirect, Blueprint
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine
livro = Blueprint('livro', __name__, template_folder='../templates')

@livro.route('/register_livros', methods=['GET', 'POST'])
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
        #f
        return redirect(url_for('index'))
    with Session(bind=engine) as db:
        lista_autores = db.execute(text("SELECT * FROM Autores"))
        lista_generos = db.execute(text("SELECT * FROM Generos"))
        lista_editoras = db.execute(text("SELECT * FROM Editoras"))
    return render_template('livros/register_livros.html', lista_generos=lista_generos, lista_editoras=lista_editoras, lista_autores=lista_autores)
