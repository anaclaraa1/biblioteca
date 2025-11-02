from flask import Flask, render_template
from config import config_app
from controllers.auth import auth_bp
from controllers.livro import livro
from controllers.genero import genero
from controllers.editora import editora
from controllers.autor import autor


app = Flask(__name__)
config_app(app)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(auth_bp)
app.register_blueprint(livro)
app.register_blueprint(genero)
app.register_blueprint(editora)
app.register_blueprint(autor)