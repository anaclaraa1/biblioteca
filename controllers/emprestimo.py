from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required, current_user
from sqlalchemy import  text
from database import engine
from datetime import date, timedelta
from controllers.livro import livros, livro

emprestimo = Blueprint('emprestimo', __name__, template_folder='../templates')


@emprestimo.route('/register_emprestimo/<int:livro_id>', methods=['GET'])
@login_required
def register_emprestimo(livro_id: int):
    with engine.begin() as conn:
        resultado = conn.execute(
                text('SELECT * FROM livros WHERE ID_livro = :livro_id'),
                {'livro_id': livro_id}
        ).fetchone()
        data_atual = date.today()
        data_futura = data_atual + timedelta(days=30)
        conn.execute(
                text('''INSERT INTO Emprestimos 
                            (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Status_emprestimo)
                        VALUES 
                            (:usuario, :livro, :data_emprestimo, :data_dev_prevista, :status)'''),
                {'usuario': current_user.id,
                 'livro':resultado.ID_livro,
                 'data_emprestimo':data_atual,
                 'data_dev_prevista': data_futura,
                 'status': 'pendente'
                 }
        )
        conn.execute(
            text('UPDATE livros SET Quantidade_disponivel = :qtd WHERE ID_livro = :id'),
                {'qtd': resultado.Quantidade_disponivel - 1, 'id': livro_id}
        )
        conn.commit()
        return redirect(url_for('livro.livros'))
