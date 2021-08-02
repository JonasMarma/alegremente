from app import db, User
import os

from flask import Flask, render_template, url_for, request, Response, redirect, make_response
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin, login_manager, LoginManager, login_user, logout_user

if os.path.exists("database.db"):
    os.remove("database.db")
db.create_all()

def addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao):
    user = User(name, email, password, tipo, plano, crp)
    user.estado = estado
    user.cidade = cidade
    user.descricao = descricao

    db.session.add(user)
    db.session.commit()

password = "123456"
crp = "06/123.456"
tipo = 1
plano = 1
descricao = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus malesuada mi et enim volutpat, sit amet sagittis mauris egestas. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur laoreet pellentesque arcu nec consectetur. Maecenas in pellentesque elit. Donec eu augue posuere, cursus nulla vitae, rhoncus diam. Nunc justo velit, vestibulum eget convallis quis, maximus sit amet erat. Fusce imperdiet odio sit amet tellus sagittis iaculis. Sed id tempor risus, auctor finibus tellus. Curabitur euismod condimentum tempus. Cras nunc ligula, ultrices eu ultricies consectetur, malesuada auctor nibh. Nunc sed posuere purus, eu luctus quam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."

name = "Nara Basílio Nunes"
email = "nara@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Jessica Alves"
email = "jessica@gmail.com"
estado = "São Paulo"
cidade = "Sorocaba"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Gilberto Fiúza Viveiros"
email = "gilberto@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Roberta Afonso"
email = "roberta@gmail.com"
estado = "Rio de Janeiro"
cidade = "Cabo Frio"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Paulo Holanda Guimarães"
email = "paulo@gmail.com"
estado = "Bahia"
cidade = "Salvador"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Ariele Laureano Alves"
email = "ariele@gmail.com"
estado = "Bahia"
cidade = "Ilhéus"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Matthias Ginjeira Amaro"
email = "matthias@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Gilson Jamandas Palma"
email = "gilson@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Túlio Frota Furquim"
email = "tulio@gmail.com"
estado = "São Paulo"
cidade = "Santo André"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Jacinto Bentes Catela"
email = "jacinto@gmail.com"
estado = "São Paulo"
cidade = "Sorocaba"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Josefa Prada Freitas"
email = "josefa@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Manuel Figueiroa Goulart"
email = "manuel@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Cristovão Ferrão Colares"
email = "cristovao@gmail.com"
estado = "Rio de Janeiro"
cidade = "Cabo Frio"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Taíssa Branco Miranda"
email = "taissa@gmail.com"
estado = "Bahia"
cidade = "Salvador"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

name = "Neymar Jr."
email = "neymar@gmail.com"
estado = "Bahia"
cidade = "Ilhéus"
addDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)