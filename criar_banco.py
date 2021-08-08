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

def addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao):
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
filename = "perfil"

crp = "06/123.456"
descricao = "Durante os ultimos 13 anos trabalhei especificamente com os transtornos mentais severos e persistentes. tal experiencia torna a prática em consultório um encontro potente e rico."
name = "Nara Basílio Nunes"
email = "nara@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/153.466"
descricao = "Amo trabalhar e ajudar pessoas...."
name = "Jessica Alves"
email = "jessica@gmail.com"
estado = "São Paulo"
cidade = "Sorocaba"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "00/143.469"
descricao = "Se você está passando por alguma dificuldade emocional, está no lugar certo. Ansiedade, depressão, estresse, incertezas com relação ao futuro abalo emocional."
name = "Gilberto Fiúza Viveiros"
email = "gilberto@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "87/156.411"
descricao = "A ansiedade, a depressão, as fobias, as manias, entre outros, são sintomas comuns para você? Tais sintomas, devem ser ouvidos como algo singular do sujeito, como aquilo que deve ser acolhido e compreendido. Realizando o processo de autoanálise, de se conhecer, será possível iniciar um trabalho em que você se torne menos dependente, mais autônomo e desenvolva da sua maneira a forma de compreender as mudanças de sua vida."
name = "Roberta Afonso"
email = "roberta@gmail.com"
estado = "Rio de Janeiro"
cidade = "Cabo Frio"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "04/321.321"
descricao = "A pandemia exigiu de cada um de nós, independente de papel social ocupado: empresário, colaborador, professor, aluno, marido, esposa, filho entre outros, uma mudança radical ao exercer nossos valores, nosso conhecimento, nossos hábitos e rotinas.  Somos seres únicos e cada um lidou e está lidando com esse desafio de forma diferente. "
name = "Paulo Holanda Guimarães"
email = "paulo@gmail.com"
estado = "Bahia"
cidade = "Salvador"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/456.789"
descricao = "Sou psicóloga clínica com 37 anos de experiência e vários cursos de especialização, tanto em Psicanálise (Freud/Lacan) como em Terapia Cognitivo Comportamental (TCC). Atendo online e também presencial em São Paulo (Perdizes) e em Santos (Boqueirão). Trabalho com ADULTOS usando a TCC que é uma terapia eficiente, rápida e focada nas dificuldades específicas do cliente."
name = "Ariele Laureano Alves"
email = "ariele@gmail.com"
estado = "Bahia"
cidade = "Ilhéus"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/321.450"
descricao = "Meu nome é Airon Bastos, sou Psicólogo registrado sob o CRP 05/64468 e credenciado para atendimentos online pelo Conselho Federal de Psicologia. Trabalho nas vertentes da Psicologia Clínica e da Psicologia do Esporte (e eSports). Algumas das atividades que desenvolvo em cada especialidade são:"
name = "Matthias Ginjeira Amaro"
email = "matthias@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/852.963"
descricao = "Sou psicólogo clínico formado em psicologia pelas Faculdades Metropolitanas Unidas, possuo pós-graduação em psicanálise pelo instituto LANGAGE,  especialização em psicossociologia pela FESPSP e especialização em linguística pela Université Catholique de Lyon (UCLY), mestrando em psicologia pela Universidad de Buenos  Aires (UBA)."
name = "Gilson Jamandas Palma"
email = "gilson@gmail.com"
estado = "São Paulo"
cidade = "São Paulo"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/174.963"
descricao = "Olá a todos!!! Meu nome é Thatianne Couto, sou Psicóloga Clínica, atuo na abordagem  Terapia cognitivo comportamental e sou formada pela Faculdade Pio Decimo. Possuo Pós-graduação em Saúde Mental, Gestão de Pessoas e Psic Organizacional e estou cursando Pós-graduação em Sexologia. Além disso, tenho Capacitação em Terapia Sexual, Capacitação em Terapia de Casal."
name = "Túlio Frota Furquim"
email = "tulio@gmail.com"
estado = "São Paulo"
cidade = "Santo André"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/025.984"
descricao = "Sou Psicologa Clinica Graduada pela Universidade Fumec, realizo atendimentos online, trabalho com a abordagem da Gestalt Terapia. A terapia é o espaço aonde você poderá falar sem receios, pois estarei ali não para julgar seus pensamentos,"
name = "Jacinto Bentes Catela"
email = "jacinto@gmail.com"
estado = "São Paulo"
cidade = "Sorocaba"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/322.466"
descricao = "Olá, como vai? Sou Psicóloga Clínica e atuo no atendimento de adultos, nas abordagens da Terapia Cognitivo Comportamental e também na DBT (Terapia Comportamental Dialética).  Meu objetivo é te ajudar a entender melhor as suas emoções, superar momentos difíceis, enfrentar seus medos e, com isso, transformar a forma como você se relaciona com a vida."
name = "Josefa Prada Freitas"
email = "josefa@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/300.466"
descricao = ""
name = "Manuel Figueiroa Goulart"
email = "manuel@gmail.com"
estado = "Rio de Janeiro"
cidade = "Rio de Janeiro"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/153.100"
descricao = "Sou psicóloga formada pela PUC-Rio e pós-graduanda em Terapia Cognitivo-Comportamental pela PUC-RS. Diversas questões e sofrimentos dificultam a nossa vida, nos prejudicam e prejudicam a nossa qualidade de vida, o meu objetivo nessa caminhada é te ajudar a lidar com essas questões e sofrimentos."
name = "Cristovão Ferrão Colares"
email = "cristovao@gmail.com"
estado = "Rio de Janeiro"
cidade = "Cabo Frio"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "07/111.200"
descricao = "Minha prática clínica é baseada na Gestalt-terapia e meu olhar será para o seu desenvolvimento com pessoa, livre de julgamentos e imposições, propiciando um espaço seguro e acolhedor para trabalhar com qualquer situação que queria trazer para o nosso processo terapêutico."
name = "Taíssa Branco Miranda"
email = "taissa@gmail.com"
estado = "Bahia"
cidade = "Salvador"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)

crp = "01/111.111"
descricao = "Atendo crianças e adultos auxiliando na Prevenção, Diagnóstico e Tratamento das Dificuldades Emocionais, Promovendo Saúde Mental e Qualidade de vida por Meio da Psicoterapia de Abordagem Psicanalítica e Avaliação Neuropsicológica."
name = "Rogério Silva"
email = "neymar@gmail.com"
estado = "Bahia"
cidade = "Ilhéus"
addPsiDummy(name, email, password, tipo, plano, crp, estado, cidade, descricao)


# Criação de perfis premium de usuário

def addUsuDummy(name, email, password, tipo, plano):
    user = User(name, email, password, tipo, plano)
    user.estado = estado
    user.cidade = cidade
    user.descricao = descricao

    db.session.add(user)
    db.session.commit()

name = "Paulo Antônio"
email = "premium1@gmail.com"
password = "123456"
tipo = 0
plano = 1
addUsuDummy(name, email, password, tipo, plano)

name = "Nathália Gomes"
email = "premium2@gmail.com"
password = "123456"
tipo = 0
plano = 1
addUsuDummy(name, email, password, tipo, plano)