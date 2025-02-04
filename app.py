from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from extensions import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 

from models import Usuario

with app.app_context():
    db.create_all()

@app.route('/user/create', methods=['POST'])
def create_user():
    dados = request.get_json()
    usuario= Usuario(
        nome=dados['nome'],
        email=dados['email']
    )

    email_existente = db.session.query(Usuario).filter_by(email=dados['email']).first()
    
    if email_existente:
        return jsonify({'Error': 'existing Email'})

    db.session.add(usuario)
    db.session.commit()
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