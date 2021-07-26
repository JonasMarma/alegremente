from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, LoginManager, login_user, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secret'

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

# Modelo no banco de dados
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(86), nullable=False, unique=True)
    password = db.Column(db.String(86), nullable=False, unique=True)
    tipo = db.Column(db.Integer, nullable=False, default=0) # 0 = cliente , 1 = psicólogo
    plano = db.Column(db.Integer, nullable=False, default=0) # 1, 2, 3 (planos basico, pro, gold, etc...)
    
    # Campos do psicólogo:
    #virtual = db.Column(db.Boolean, nullable=True)
    crp = db.Column(db.String(86), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    estado = db.Column(db.String(40), nullable=True)
    cidade = db.Column(db.String(40), nullable=True)
    endereco = db.Column(db.String(40), nullable=True)
    maps = db.Column(db.String(40), nullable=True)

    # Campos do usuário

    def __init__(self, name, email, password, tipo, plano, crp='0'):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.tipo = tipo
        self.plano = plano
        self.crp = crp

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    # Retornar uma string ao criar um elemento
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET'])
def index():
    usuarios = User.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            print('Usuário não encontrado')
            return redirect(url_for('login'))

        if  not user.verify_password(pwd):
            print('Senha incorreta')
            return redirect(url_for('login'))

        print('Logou')
        login_user(user)

        if user.tipo == 1:
            return render_template('dashboardpsi.html')
        else:
            return render_template('index.html')

    return render_template('login.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        tipo = 1
        plano = 0
        crp = request.form['crp']

        #if name and email and password and crp:
        user = User(name, email, password, tipo, plano, crp)

        db.session.add(user)
        db.session.commit()

    return redirect(url_for('index'))
        
    #return redirect(url_for('index'))

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    return render_template('cadastro-psi.html')

@app.route('/planospsi/')
def planospsi():
    return render_template('planospsi.html')

@app.route('/updateperfilpsi/<int:id>', methods=['GET', 'POST'])
def updateperfilpsi(id):

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        
        user.name = request.form['name']
        user.email = request.form['email']
        #password = db.Column(db.String(86), nullable=False, unique=True)
        #user.plano = db.Column(db.Integer, nullable=False, default=0) # 1, 2, 3 (planos basico, pro, gold, etc...)

        # Campos do psicólogo:
        #virtual = db.Column(db.Boolean, nullable=True)
        user.crp = request.form['crp']
        user.descricao = request.form['descricao']
        user.telefone = request.form['telefone']
        user.celular = request.form['celular']
        user.whatsapp = request.form['whatsapp']
        user.estado = request.form['estado']
        user.cidade = request.form['cidade']
        user.endereco = request.form['endereco']
        user.maps = request.form['maps']

        try:
            db.session.commit()
            return redirect('dashboardpsi.html')
        except:
            return('Houve um erro ao atualizar ;-;')

    else:
        return render_template('update.html', task=task)
'''
# Deletando pela chave primária id
@app.route('/delete/<int:id>')
def delete(id):
    # Tentar pegar a task pelo id ou retornar 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um problema interno ao deletar'

'''

if __name__ == "__main__":
    app.run(debug=True)