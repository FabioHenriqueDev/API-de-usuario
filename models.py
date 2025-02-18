from extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(140), unique=True, nullable=False)
    senha = db.Column(db.String(140), nullable=False)

class CodigoVerificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    email_usuario = db.Column(db.String(140), db.ForeignKey('usuario.email'), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)