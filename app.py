from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import re

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 
CORS(app)

bcrypt = Bcrypt(app)

from models import Usuario

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/user/create', methods=['POST'])
def create_user():
    dados = request.get_json()

    if 'nome' not in dados or not dados['nome']:
        return jsonify({'Error': 'O Nome é Obrigatório'})

    
    if 'email' not in dados or not dados['email']:
        return jsonify({'Error': 'O E-mail é Obrigatório'})


    if 'senha' not in dados or not dados['senha']:
        return jsonify({'Error': 'Senha é Obrigatória'})
    
    
    if len(dados['nome']) < 2:
        return jsonify({'Error': 'O Username tem que ter no mínimo 2 caracteres'})


    if len(dados['senha']) < 6:
        return jsonify({'Error': 'A senha deve ter mais que 5 caracteres'})
    
    email_padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_padrao, dados['email']):
        return jsonify({'Erro': 'Digite um E-mail válido'})

    senha_criptografada = bcrypt.generate_password_hash(dados['senha'])

    usuario= Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha=senha_criptografada
    )


    email_existente = db.session.query(Usuario).filter_by(email=dados['email']).first()
    
    if email_existente:
        return jsonify({'Error': 'existing Email'})
    

     # Configurações do servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ["email"]
    sender_password = os.environ["senha_app"]

    # Compondo o e-mail
    msg = MIMEMultipart()
    msg['Subject'] = 'Bem-vindo(a) ao nosso sistema! 🎉'
    msg['From'] = sender_email
    msg['To'] = dados['email']


    html = f"""
            <html>
            <body style="font-family: Arial">
                <h1 style="color: blue;">Olá {dados['nome']},</h1>
                <img src="https://i.pinimg.com/736x/27/68/3e/27683e7872af4e367e2f27e9efdd1993.jpg" alt="Boas-Vindas" style="width:100%;max-width:600px;height:auto;">
                <h2>Obrigado por se cadastrar no nosso sistema! Estamos muito felizes em tê-lo(a) conosco.</h2>
                <h3>Aqui estão algumas coisas que você pode fazer agora:</h3>
                <ul>
                    <li>Explorar nossos conteúdos exclusivos.</li>
                    <li>Personalizar seu perfil e preferências.</li>
                    <li>Aproveitar as promoções e ofertas especiais.</li>
                </ul>
                <h3>Se precisar de ajuda ou tiver alguma dúvida, nossa equipe de suporte está sempre pronta para ajudar. Não hesite em entrar em contato!</h3>
                <h4>Mais informações sobre o quem desenvolveu essa API clique nesse <a href="https://github.com/FabioHenriqueDev">link</a></h4>
                <p style="color: gray;">Tenha um ótimo dia!</p>
            </body>
            </html>
        """

    msg.attach(MIMEText(html, 'html'))

    db.session.add(usuario)
    db.session.commit()
    
    # Enviando o e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print('Email Enviado com Sucesso')

    except:
        print('Erro ao envio do E-mail')

   

    return jsonify({'mensage': 'User created'})



@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    usuario = Usuario.query.get(id)
    
    if usuario:
        return jsonify({'ID': f'{usuario.id}', 'Nome': f'{usuario.nome}', 'Email': f'{usuario.email}'})
    
    else:
        return jsonify({'Error': 'Not Found'})
    

@app.route('/user/todos', methods=['GET'])
def mostrar_usuarios():
    lista_usuarios =  Usuario.query.all()
    usuarios_dados = [{'Nome': usuario.nome} for usuario in lista_usuarios]
    return jsonify(usuarios_dados)



@app.route('/user/atualizar/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    dados = request.get_json()

    if not usuario:
        return jsonify({'Error': 'User not found'})
    
    if 'nome' in dados:
        usuario.nome = dados['nome']
    
    if 'email' in dados:
        usuario.email = dados['email']
    
    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso"})



@app.route('/user/excluir/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)

    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'Sucess': 'User deleted'})

    else:
        return jsonify({'Error': 'User not Found'})




app.run(debug=True)