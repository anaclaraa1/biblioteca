from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
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
        try:
            with Session(bind=engine) as db:
                db.execute(text("SET @usuario_logado_id = :uid"), {
                        "uid": current_user.id})
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
            flash('Livro cadastrado com sucesso!', category='success')
            return redirect(url_for('livro.livros'))
        
        except OperationalError as e:
            flash(e.orig.args[1], category='error') # Mensagem de erro do banco de dados
            return redirect(url_for('livro.register_livros'))
    
    with Session(bind=engine) as db:
        lista_autores = db.execute(text("SELECT * FROM Autores")).fetchall()
        lista_generos = db.execute(text("SELECT * FROM Generos")).fetchall()
        lista_editoras = db.execute(text("SELECT * FROM Editoras")).fetchall()

    return render_template('livros/register_livros.html', lista_generos=lista_generos, lista_editoras=lista_editoras, lista_autores=lista_autores)


@livro.route('/editar_livro/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def editar_livro(livro_id: int):
    if request.method == 'POST':
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE livros
                        SET Titulo = :Titulo,
                        Autor_id = :Autor_id,
                        ISBN = :ISBN,
                        Ano_publicacao = :Ano_publicacao,
                        Genero_id = :Genero_id,
                        Editora_id = :Editora_id,
                        Quantidade_disponivel = :Quantidade_disponivel,
                        Resumo = :Resumo
                        WHERE ID_livro = :livro_id
                    '''
                ),
                {**request.form, 'livro_id': livro_id}
            )
            conn.commit()
        flash('Livro alterado com sucesso', category='success')
        return redirect(url_for('livro.livros'))

    with engine.begin() as conn:
        livro = conn.execute(
            text('SELECT * FROM livros WHERE ID_livro = :livro_id'),
            {'livro_id': livro_id}
        ).fetchone()
        autores = conn.execute(text('SELECT * FROM autores'))
        generos = conn.execute(text('SELECT * FROM generos'))
        editoras = conn.execute(text('SELECT * FROM editoras'))
    return render_template('livros/editar_livro.html', livro=livro, autores=autores, generos=generos, editoras=editoras)


@livro.route('/deletar_livros/<int:livro_id>')
@login_required
def deletar_livros(livro_id: int):
    with engine.begin() as conn:
        try:
            conn.execute(text("SET @usuario_logado_id = :uid"), {
                "uid": current_user.id})
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
            flash('Não é possível deletar o livro...', category='error')
        else:
            flash('Livro deletado com sucesso!', category='success')
    return redirect(url_for('livro.livros'))

@livro.route('/historico_livros', methods=['GET'])
@login_required
def historico_livros():
    with engine.begin() as conn:
        livros_delete = conn.execute(text("SELECT * FROM Historico_Livro JOIN Autores on Autores.ID_autor = Historico_livro.Autor_id JOIN Editoras on Editoras.ID_editora = Historico_livro.Editora_id JOIN Generos on Generos.ID_genero=Historico_livro.Genero_id JOIN Usuarios on Usuarios.ID_Usuario = Historico_livro.Usuario_id where Acao = 'DELETE'")).all()
        
        
        return render_template('livros/historico_livros.html', livros_delete=livros_delete)
        
     