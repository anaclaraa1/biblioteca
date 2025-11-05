from flask import render_template, Blueprint
from flask_login import login_required, current_user
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