from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from extensions import db, jwt
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import re
from flask_jwt_extended import create_access_token, create_refresh_token


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 
CORS(app)
jwt.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

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
    smtp_server = 'smtp.gmail.com' # variavel de ambiente
    smtp_port = 587 # variavel de ambiente
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

    try:
        db.session.add(usuario) 
        db.session.commit()
    
    except:
        return jsonify({'Erro': 'Não foi possível adicionar o usuário'})
    
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


@app.route('/login', methods=['POST'])
def login():
    
    dados = request.get_json()

    usuario = Usuario.query.filter_by(email=dados['email']).first()
   
    if not usuario:
        return jsonify({'Erro': 'E-mail ou Senha incorretos'}), 401

    if not bcrypt.check_password_hash(usuario.senha, dados['senha']):
        return jsonify({'Erro': 'E-mail ou Senha incorretos'}), 401

    token_acesso = create_access_token(identity=usuario.email)
    token_atualizacao = create_refresh_token(identity=usuario.email)

    
    return jsonify(
                    {
                        'mensage': 'Login feito com sucesso',
                        'usuario': usuario.nome,
                        'tokens': {
                            "acesso": token_acesso,
                            'atualização': token_atualizacao
                        }
                    }
                ) , 200




@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    usuario = Usuario.query.get(id)
    
    if usuario:
        return jsonify({'ID': f'{usuario.id}', 'Nome': f'{usuario.nome}', 'Email': f'{usuario.email}'})
    
    else:
        return jsonify({'Erro': 'Usuario não encontrado'})
    

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
        return jsonify({'Error': 'Usuario nao Encontrado'})

    usuario_msm_nome = usuario.nome == dados['nome']
    usuario_msm_email = usuario.email == dados['email']
    usuario_msm_senha = bcrypt.check_password_hash(usuario.senha, dados['senha'])


    if usuario_msm_nome and usuario_msm_email and usuario_msm_senha:
        return jsonify({'Erro': 'Faça alguma mudança antes de enviar'})

    email_padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_padrao, dados['email']):
        return jsonify({'Erro': 'Digite um E-mail válido'})
  
    if 'nome' in dados and dados['nome']:
        usuario.nome = dados['nome']
    
    else:
        return jsonify({'Erro': 'Digite o nome de usuario para atualizar'})
    
    if 'email' in dados and dados['email']:
        usuario.email = dados['email']
    
    else:
        return jsonify({'Erro': 'Digite o E-mail para atualizar'})
    
    if 'senha' in dados and dados['senha']:
        usuario.senha = bcrypt.generate_password_hash(dados['senha'])
    
    else:
        return jsonify({'Erro': 'Digite a senha para alterar'})

    if len(dados['nome']) < 2:
        return jsonify({'Error': 'O Nome tem que ter no mínimo 2 caracteres'})


    if len(dados['senha']) < 6:
        return jsonify({'Error': 'A senha deve ter mais que 5 caracteres'})
    
    try:
        db.session.commit()
    
    except:
        return jsonify({'Erro': 'Não foi possível adicionar o usuário'})

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ["email"]
    sender_password = os.environ["senha_app"]

    # Compondo o e-mail
    msg = MIMEMultipart()
    msg['Subject'] = 'Suas Informações Foram Atualizadas com Sucesso ✅'
    msg['From'] = sender_email
    msg['To'] = dados['email']

    html = f"""
            <html>
            <body style="font-family: Arial">
                <h1 style="color: blue;">Olá {dados['nome']},</h1>
                <h2>Gostaríamos de informar que algumas informações na sua conta foram atualizadas com sucesso:</h2>
                <ul>
                    <li><b>Email:</b> {dados['email']}</li>
                    <li><b>Nome:</b> {dados['nome']}</li>
                    <li><b>Senha:</b> {dados['senha']}</li>
                </ul>
                <h3>Se você não solicitou essas alterações, por favor, entre em contato conosco imediatamente para garantirmos a segurança da sua conta.</h3>
                <h4>Agradecemos pela sua atenção e estamos à disposição para qualquer dúvida.</a></h4>
                <p style="color: gray;">Atenciosamente, Sistema</p>
            </body>
            </html>
        """

    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print('Email Enviado com Sucesso')

    except:
        ('Erro ao envio do E-mail')

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