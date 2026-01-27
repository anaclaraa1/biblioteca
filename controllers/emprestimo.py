from flask import render_template, url_for, request,redirect, Blueprint, flash
from flask_login import login_required, current_user
from sqlalchemy import  text
from sqlalchemy.exc import  OperationalError
from database import engine
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
emprestimo = Blueprint('emprestimo', __name__, template_folder='../templates')


@emprestimo.route('/register_emprestimo/<int:livro_id>', methods=['GET'])
@login_required
def register_emprestimo(livro_id: int):
    try:
        with engine.begin() as conn:
            resultado = conn.execute(
                    text('SELECT * FROM livros WHERE ID_livro = :livro_id'),
                    {'livro_id': livro_id}
            ).fetchone()
            conn.execute(
                text('''
                    INSERT INTO Emprestimos (Usuario_id, Livro_id)
                    VALUES (:usuario, :livro)
                '''),
                {
                    'usuario': current_user.id,
                    'livro': resultado.ID_livro  # type: ignore
                }
            )

            conn.commit()
            flash('Livro reservado com sucesso!', category='success')
            return redirect(url_for('livro.livros'))
    except OperationalError as e:
        flash(e.orgin.args[1], category='error') # Mensagem de erro do banco de dados
        return redirect(url_for('livro.livros'))

@emprestimo.route('/emprestimos', methods=['GET'])
@login_required
def visualizar():
    user_id = current_user.id
    with engine.begin() as conn:
        data = conn.execute(
            text('''SELECT * FROM emprestimos JOIN livros ON livros.ID_livro = emprestimos.Livro_id WHERE Usuario_id = :user_id'''),
            {'user_id': user_id}
        )
        emprestimos = data.all()

    return render_template('emprestimos/listar_emprestimo.html', emprestimos=emprestimos)

@emprestimo.route('/devolucao/<int:emprestimo_id>', methods=['GET'])
def devolucao(emprestimo_id: int):
    with engine.begin() as conn:
        
        data_devolucao_real = date.today()
        
        conn.execute(
            text('''
                UPDATE emprestimos SET
                Status_emprestimo = 'devolvido',
                Data_devolucao_real = :data
                WHERE ID_emprestimo = :emprestimo_id'''),
            {'emprestimo_id': emprestimo_id, 'data': data_devolucao_real}
        )

        flash('Livro devolvido com sucesso!', category='success')
        return redirect(url_for('emprestimo.visualizar'))
    
@emprestimo.route('/editar_emprestimo/<int:emprestimo_id>', methods=['GET', 'POST'])
def editar_emprestimo(emprestimo_id: int):
    if request.method == 'POST':
        data_real = request.form['Data_devolucao_real']
        if not data_real:
            data_real = None
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE emprestimos SET Data_emprestimo = :Data_emprestimo, Data_devolucao_prevista = :Data_devolucao_prevista, Data_devolucao_real = :Data_devolucao_real WHERE ID_emprestimo = :emprestimo_id
                    '''
                ),
                {
                    **request.form,
                    'Data_devolucao_real': data_real, 
                    'emprestimo_id': emprestimo_id
                }
            )
            conn.commit()

        flash('Dados alterados com sucesso!', category='success')
        return redirect(url_for('emprestimo.visualizar'))
    
    with engine.begin() as conn:
        emprestimo = conn.execute(
            text('''SELECT * FROM emprestimos WHERE ID_emprestimo = :emprestimo_id'''),
            {'emprestimo_id': emprestimo_id}
        ).fetchone()
        
    return render_template('emprestimos/editar_emprestimo.html', emprestimo=emprestimo)

@emprestimo.route('/deletar_emprestimo/<int:emprestimo_id>', methods=['GET'])
def deletar_emprestimo(emprestimo_id: int):
    with engine.begin() as conn:
        data = conn.execute(
            text('SELECT * FROM emprestimos WHERE ID_emprestimo = :emprestimo_id'),
            {'emprestimo_id': emprestimo_id}
        ).fetchone()
        
        if data is None:
            flash('Empréstimo não encontrado.', category='error')
            return redirect(url_for('emprestimo.visualizar'))
        if data[6] != 'devolvido':
            flash('Só é possível deletar empréstimos que já foram devolvidos.', category='error')
            return redirect(url_for('emprestimo.visualizar'))

        try:
            conn.execute(
                text(
                    '''
                        delete from emprestimos where ID_emprestimo = :emprestimo_id
                    '''
                ),
                {'emprestimo_id': emprestimo_id}
            )
            conn.commit()
        except IntegrityError:
            flash('Não é possível deletar o emprestimo...', category='error')
        else:
            flash('Emprestimo deletado com sucesso!', category='success')
    return redirect(url_for('emprestimo.visualizar'))