from flask import Flask, render_template, url_for, request, Response, redirect, make_response
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(86), nullable=False, unique=True)
    password = db.Column(db.String(86), nullable=False, unique=True)
    tipo = db.Column(db.Integer, nullable=False, default=0) # 0 = cliente , 1 = psicólogo
    plano = db.Column(db.Integer, nullable=False, default=0) # 1, 2, 3 (planos basico, pro, gold, etc...)
    
    # Campos do psicólogo:
    img = db.Column(db.Text, unique=True, nullable=True)
    imgname = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)

    crp = db.Column(db.String(86), nullable=True)
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
        return '<ID: %r>' % self.id

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
            return redirect(url_for('login'))

        if  not user.verify_password(pwd):
            return redirect(url_for('login'))
            
        login_user(user)

        if user.tipo == 1:
            return render_template('dashboardpsi.html')
        else:
            return render_template('index.html')

    return render_template('login.html')

@app.route('/loginusu/', methods=['GET', 'POST'])
def loginusu():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('loginusu'))

        if  not user.verify_password(pwd):
            return redirect(url_for('loginusu'))
            
        login_user(user)

        return render_template('mobile/menu.html')

    return render_template('mobile/login.html')

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/logoutusu/', methods=['GET', 'POST'])
def logoutusu():
    logout_user()
    return render_template('mobile/menu.html')

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
            #return redirect('dashboardpsi.html')
            return render_template('dashboardpsi.html')
        except:
            return('Houve um erro ao atualizar ;-;')

    else:
        return render_template('update.html', task=task)

@app.route('/uploadimg/<int:id>', methods=['POST'])
def upload(id):
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    #img = Img(img=pic.read(), imgname=filename, mimetype=mimetype)

    user = User.query.get_or_404(id)

    user.img = pic.read()
    user.imgname = filename
    user.mimetype = mimetype
    #db.session.add(img)
    db.session.commit()

    return render_template('dashboardpsi.html')

@app.route('/image/<int:id>', methods=['GET','POST'])
def image(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return 'Img Not Found!', 404

    return Response(user.img, mimetype=user.mimetype)


@app.route('/mobile/')
def mobile():

    entrou = request.cookies.get('entrou')

    print(str(entrou))

    if (entrou == None):
        print('Primeira vez')
        resp = make_response(render_template('mobile/mobile.html'))
        resp.set_cookie('entrou', "1", expires=2147483647)
        return resp
    else:
        print("Não primeira vez")
        return redirect(url_for('mobilemenu'))

@app.route('/mobilequestionario/')
def mobilequestionario():
    return render_template('mobile/questionario/questionario.html')

@app.route('/mobilemenu/')
def mobilemenu():
    return render_template('mobile/menu.html')

@app.route('/mobilepesquisapsicologos/' , methods=['GET', 'POST'])
def mobilepsicologos():

    if request.method == 'GET':
        # Puxar os estados distintos com cadastros
        queryEstados = db.session.query(User.estado.distinct())
        
        estados = []

        # Pai, me perdoa, eu não sei o que faço!

        acre = []
        alagoas = []
        amapa = []
        amazonas = []
        bahia = []
        ceara = []
        espiritosanto = []
        goias = []
        maranhao = []
        matogrosso = []
        matogrossodosul = []
        minasgerais = []
        para = []
        paraiba = []
        parana = []
        pernambuco = []
        piaui = []
        riodejaneiro = []
        riograndedonorte = []
        riograndedosul = []
        rondonia = []
        roraima = []
        santacatarina = []
        saopaulo = []
        sergipe = []
        tocantins = []
        distritofederal = []

        for e in queryEstados.all():
            estados.append(e[0])

        for estado in estados:
            # Puxar as cidades com cadastros para o estado
            queryCidades = db.session.query(User.cidade.distinct()).filter(User.estado.like(estado))
            for c in queryCidades.all():
                if (estado == "Acre"):
                    acre.append(c[0])
                elif (estado =="Alagoas"):
                    alagoas.append(c[0])
                elif (estado == "Amapá"):
                    amapa.append(c[0])
                elif (estado == "Amazonas"):
                    amazonas.append(c[0])
                elif (estado == "Bahia"):
                    bahia.append(c[0])
                elif (estado == "Ceará"):
                    ceara.append(c[0])
                elif (estado == "Espírito Santo"):
                    espiritosanto.append(c[0])
                elif (estado == "Goiás"):
                    goias.append(c[0])
                elif (estado == "Maranhão"):
                    maranhao.append(c[0])
                elif (estado == "Mato Grosso"):
                    matogrosso.append(c[0])
                elif (estado == "Mato Grosso do Sul"):
                    matogrossodosul.append(c[0])
                elif (estado == "Minas Gerais"):
                    minasgerais.append(c[0])
                elif (estado == "Pará"):
                    para.append(c[0])
                elif (estado == "Paraíba"):
                    paraiba.append(c[0])
                elif (estado == "Paraná"):
                    parana.append(c[0])
                elif (estado == "Pernambuco"):
                    pernambuco.append(c[0])
                elif (estado == "Piauí"):
                    piaui.append(c[0])
                elif (estado == "Rio de Janeiro"):
                    riodejaneiro.append(c[0])
                elif (estado == "Rio Grande do Norte"):
                    riograndedonorte.append(c[0])
                elif (estado == "Rio Grande do Sul"):
                    riograndedosul.append(c[0])
                elif (estado == "Rondônia"):
                    rondonia.append(c[0])
                elif (estado == "Roraima"):
                    roraima.append(c[0])
                elif (estado == "Santa Catarina"):
                    santacatarina.append(c[0])
                elif (estado == "São Paulo"):
                    saopaulo.append(c[0])
                elif (estado == "Sergipe"):
                    sergipe.append(c[0])
                elif (estado == "Tocantins"):
                    tocantins.append(c[0])
                elif (estado == "Distrito Fedral"):
                    distritofederal.append(c[0])

        # Exemplo:
        #estados = ['São Paulo', 'Rio de Janeiro', 'Bahia']
        #saopaulo = ['São Paulo', 'Sorocaba', 'Santo André']

        return render_template('mobile/psicologos/pesquisapsicologos.html', estados=estados,
                                                                            acre=acre,
                                                                            alagoas=alagoas,
                                                                            amapa=amapa,
                                                                            amazonas=amazonas,
                                                                            bahia=bahia,
                                                                            ceara=ceara,
                                                                            espiritosanto=espiritosanto,
                                                                            goias=goias,
                                                                            maranhao=maranhao,
                                                                            matogrosso=matogrosso,
                                                                            matogrossodosul =matogrossodosul,
                                                                            minasgerais=minasgerais,
                                                                            para=para,
                                                                            paraiba=paraiba,
                                                                            parana=parana,
                                                                            pernambuco=pernambuco,
                                                                            piaui=piaui,
                                                                            riodejaneiro=riodejaneiro,
                                                                            riograndedonorte=riograndedonorte,
                                                                            riograndedosul=riograndedosul,
                                                                            rondonia=rondonia,
                                                                            roraima=roraima,
                                                                            santacatarina=santacatarina,
                                                                            saopaulo=saopaulo,
                                                                            sergipe=sergipe,
                                                                            tocantins=tocantins,
                                                                            distritofederal=distritofederal)

    if request.method == 'POST':
        #estadoSelect = request.form.get('estado')
        cidadeSelect = request.form.get('cidade')

        resultadoQuery = db.session.query(User).filter_by(cidade=cidadeSelect)

        return render_template('mobile/psicologos/listapsi.html', cidade=cidadeSelect, resultadoQuery=resultadoQuery)

@app.route('/mobilelistapsi/<string:estadocidade>', methods=['GET', 'POST'])
def mobilelistapsi(cidade, resultadoQuery):
    if request.method == 'GET':
        return render_template('mobile/psicologos/listapsi.html')
    
    if request.method == 'POST':
        return render_template('mobile/psicologos/listapsi.html', resultadoQuery=resultadoQuery)


@app.route('/mobileverperfil/<int:id>', methods=['GET', 'POST'])
def mobileverperfil(id):
    
    psi = User.query.get_or_404(id)

    return render_template('mobile/psicologos/verperfil.html', psi=psi)

@app.route('/mobileblogs/')
def mobileblogs():
    return render_template('mobile/blogs.html')

# VIDEOS MOBILE
@app.route('/mobilevideos/')
def mobilevideos():
    return render_template('mobile/videos/videos.html')

@app.route('/mobilevideoscovid/')
def mobilevideoscovid():
    return render_template('mobile/videos/videoscovid.html')

@app.route('/mobilevideossocial/')
def mobilevideossocial():
    return render_template('mobile/videos/videossocial.html')

@app.route('/mobilevideosmente/')
def mobilevideosmente():
    return render_template('mobile/videos/videosmente.html')

@app.route('/mobilevideossaude/')
def mobilevideossaude():
    return render_template('mobile/videos/videossaude.html')

@app.route('/mobilevideosdepressao/')
def mobilevideosdepressao():
    return render_template('mobile/videos/videosdepressao.html')

@app.route('/mobilevideosansiedade/')
def mobilevideosansiedade():
    return render_template('mobile/videos/videosansiedade.html')

@app.route('/mobilevideosdrogas/')
def mobilevideosdrogas():
    return render_template('mobile/videos/videosdrogas.html')

@app.route('/mobilerespiracao/')
def mobilerespiracao():
    return render_template('mobile/respiracao.html')

@app.route('/premium/')
def premium():
    return render_template('mobile/premium.html')

# ------- SITE ----------

@app.route('/respiracao/')
def respiracao():
    return render_template('respiracao.html')

@app.route('/landingpageapp/')
def landingpageapp():
    return render_template('landingpageapp.html')


@app.route('/blogs/')
def blogs():
    return render_template('blogs.html')

@app.route('/database/')
def database():
    return render_template('database.html')

# VÍDEOS SITE
@app.route('/videos/')
def videos():
    return render_template('videos/videos.html')

@app.route('/videoscovid/')
def videoscovid():
    return render_template('videos/videoscovid.html')

@app.route('/videossocial/')
def videossocial():
    return render_template('videos/videossocial.html')

@app.route('/videosmente/')
def videosmente():
    return render_template('videos/videosmente.html')

@app.route('/videossaude/')
def videossaude():
    return render_template('videos/videossaude.html')

@app.route('/videosdepressao/')
def videosdepressao():
    return render_template('videos/videosdepressao.html')

@app.route('/videosansiedade/')
def videosansiedade():
    return render_template('videos/videosansiedade.html')

@app.route('/videosdrogas/')
def videosdrogas():
    return render_template('videos/videosdrogas.html')


@app.route('/pagamentopremium/')
def pagamentopremium():
    return render_template('pagamentopremium.html')

# Pesquisa sobre os psicólogos
@app.route('/psicologos/' , methods=['GET', 'POST'])
def psicologos():

    if request.method == 'GET':
        # Puxar os estados distintos com cadastros
        queryEstados = db.session.query(User.estado.distinct())
        
        estados = []

        # Pai, me perdoa, eu não sei o que faço!

        acre = []
        alagoas = []
        amapa = []
        amazonas = []
        bahia = []
        ceara = []
        espiritosanto = []
        goias = []
        maranhao = []
        matogrosso = []
        matogrossodosul = []
        minasgerais = []
        para = []
        paraiba = []
        parana = []
        pernambuco = []
        piaui = []
        riodejaneiro = []
        riograndedonorte = []
        riograndedosul = []
        rondonia = []
        roraima = []
        santacatarina = []
        saopaulo = []
        sergipe = []
        tocantins = []
        distritofederal = []

        for e in queryEstados.all():
            estados.append(e[0])

        for estado in estados:
            # Puxar as cidades com cadastros para o estado
            queryCidades = db.session.query(User.cidade.distinct()).filter(User.estado.like(estado))
            for c in queryCidades.all():
                if (estado == "Acre"):
                    acre.append(c[0])
                elif (estado =="Alagoas"):
                    alagoas.append(c[0])
                elif (estado == "Amapá"):
                    amapa.append(c[0])
                elif (estado == "Amazonas"):
                    amazonas.append(c[0])
                elif (estado == "Bahia"):
                    bahia.append(c[0])
                elif (estado == "Ceará"):
                    ceara.append(c[0])
                elif (estado == "Espírito Santo"):
                    espiritosanto.append(c[0])
                elif (estado == "Goiás"):
                    goias.append(c[0])
                elif (estado == "Maranhão"):
                    maranhao.append(c[0])
                elif (estado == "Mato Grosso"):
                    matogrosso.append(c[0])
                elif (estado == "Mato Grosso do Sul"):
                    matogrossodosul.append(c[0])
                elif (estado == "Minas Gerais"):
                    minasgerais.append(c[0])
                elif (estado == "Pará"):
                    para.append(c[0])
                elif (estado == "Paraíba"):
                    paraiba.append(c[0])
                elif (estado == "Paraná"):
                    parana.append(c[0])
                elif (estado == "Pernambuco"):
                    pernambuco.append(c[0])
                elif (estado == "Piauí"):
                    piaui.append(c[0])
                elif (estado == "Rio de Janeiro"):
                    riodejaneiro.append(c[0])
                elif (estado == "Rio Grande do Norte"):
                    riograndedonorte.append(c[0])
                elif (estado == "Rio Grande do Sul"):
                    riograndedosul.append(c[0])
                elif (estado == "Rondônia"):
                    rondonia.append(c[0])
                elif (estado == "Roraima"):
                    roraima.append(c[0])
                elif (estado == "Santa Catarina"):
                    santacatarina.append(c[0])
                elif (estado == "São Paulo"):
                    saopaulo.append(c[0])
                elif (estado == "Sergipe"):
                    sergipe.append(c[0])
                elif (estado == "Tocantins"):
                    tocantins.append(c[0])
                elif (estado == "Distrito Fedral"):
                    distritofederal.append(c[0])

        # Exemplo:
        #estados = ['São Paulo', 'Rio de Janeiro', 'Bahia']
        #saopaulo = ['São Paulo', 'Sorocaba', 'Santo André']

        return render_template('psicologos/pesquisapsicologos.html', estados=estados,
                                                                            acre=acre,
                                                                            alagoas=alagoas,
                                                                            amapa=amapa,
                                                                            amazonas=amazonas,
                                                                            bahia=bahia,
                                                                            ceara=ceara,
                                                                            espiritosanto=espiritosanto,
                                                                            goias=goias,
                                                                            maranhao=maranhao,
                                                                            matogrosso=matogrosso,
                                                                            matogrossodosul =matogrossodosul,
                                                                            minasgerais=minasgerais,
                                                                            para=para,
                                                                            paraiba=paraiba,
                                                                            parana=parana,
                                                                            pernambuco=pernambuco,
                                                                            piaui=piaui,
                                                                            riodejaneiro=riodejaneiro,
                                                                            riograndedonorte=riograndedonorte,
                                                                            riograndedosul=riograndedosul,
                                                                            rondonia=rondonia,
                                                                            roraima=roraima,
                                                                            santacatarina=santacatarina,
                                                                            saopaulo=saopaulo,
                                                                            sergipe=sergipe,
                                                                            tocantins=tocantins,
                                                                            distritofederal=distritofederal)
        #return render_template('psicologos/pesquisapsicologos.html')

    if request.method == 'POST':
        estadoSelect = request.form.get('estado')
        cidadeSelect = request.form.get('cidade')

        resultadoQuery = db.session.query(User).filter_by(cidade=cidadeSelect)

        return render_template('psicologos/listapsi.html', cidade=cidadeSelect, resultadoQuery=resultadoQuery)

@app.route('/listapsi/<string:estadocidade>', methods=['GET', 'POST'])
def listapsi(cidade, resultadoQuery):
    if request.method == 'GET':
        return render_template('mobile/psicologos/listapsi.html')
    
    if request.method == 'POST':
        return render_template('psicologos/listapsi.html', resultadoQuery=resultadoQuery)


@app.route('/verperfil/<int:id>', methods=['GET', 'POST'])
def verperfil(id):
    
    psi = User.query.get_or_404(id)

    return render_template('psicologos/verperfil.html', psi=psi)

if __name__ == "__main__":
    app.run(debug=True)