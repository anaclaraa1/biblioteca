from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from database import engine
from sqlalchemy import text


perfil = Blueprint('perfil', __name__, template_folder='../templates')


@perfil.route('/perfil', methods=['GET'])
@login_required
def visualizar():
    user_id = current_user.id
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM usuarios WHERE ID_usuario = :user_id'), {'user_id': user_id})
        user = data.fetchone()
        
    return render_template('user/perfil.html', user=user)


@perfil.route('/editar_perfil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(user_id: int):
    if request.method == 'POST':
        with engine.begin() as conn:
            conn.execute(
                text(
                    '''
                        UPDATE usuarios
                        SET Nome_usuario = :nome,
                        Email = :email,
                        Numero_telefone = :tel
                        WHERE ID_usuario = :user_id
                    '''
                ),
                {**request.form, 'user_id': user_id}
            )
            conn.commit()
        flash('Dados alterados com sucesso!', category='success')
        return redirect(url_for('perfil.visualizar'))
    
    with engine.begin() as conn:
        data = conn.execute(text('SELECT * FROM usuarios WHERE ID_usuario = :user_id'), {'user_id': user_id})
        user = data.fetchone()
    return render_template('user/editar.html', user=user)


@perfil.route('/deletar_perfil/<int:user_id>', methods=['GET'])
@login_required
def deletar_perfil(user_id: int):
    with engine.begin() as conn:
        conn.execute(
            text('DELETE FROM emprestimos WHERE Usuario_id = :user_id'),
            {'user_id': user_id}
        )
        conn.execute(
            text('DELETE FROM usuarios WHERE ID_usuario = :user_id'),
            {'user_id': user_id}
        )
        conn.commit()
    logout_user()
    return redirect(url_for('index'))
