from flask import render_template, url_for, request,redirect, Blueprint
from sqlalchemy.orm import Session
from sqlalchemy import  text
from database import engine
genero = Blueprint('genero', __name__, template_folder='../templates')

@genero.route('/register_generos', methods=['GET', 'POST'])
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
                # f
                return redirect(url_for('index'))
            # f
    return render_template('generos/register_genero.html')
