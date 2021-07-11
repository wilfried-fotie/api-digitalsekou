from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

CONNECT = f"mysql+pymysql://{secrets.dbuser}:{secrets.dbpass}@{secrets.dbhost}/{secrets.dbname}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET-KEY"
db = SQLAlchemy(app)


class Etablissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    profil = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sigle = db.Column(db.String(40), unique=True, nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    pro = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    filiaire = db.relationship('Filiaire', backref='etablissement', lazy=True)
    statistiques = db.relationship('Statistiques', backref="etablissement", lazy=True)
    messages = db.relationship('Messages', backref="etablissement", lazy=True)
    filiaire = db.relationship('Filiaire', backref="etablissement", lazy=True)
    specialite = db.relationship('Specialite', backref="etablissement", lazy=True)
    pubSchool = db.relationship('PubSchool', backref="etablissement", lazy=True)


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, password, tel, description, position, sigle, logo, profil, pro):
        self.name = name
        self.position = position
        self.password = password
        self.tel = tel
        self.description = description
        self.sigle = sigle
        self.logo = logo
        self.profil = profil
        self.pro = pro

    def __repr__(self):
        return f'<Etablissement {self.sigle} >'


class Filiaire(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    etablissement_id = db.Column(db.Integer, db.ForeignKey("etablissement.id"), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, etablissement_id):
        self.name = name
        self.etablissement_id = etablissement_id

    def __repr__(self):
        return f'<Filiaire {self.sigle} >'



class Specialite(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    filiaire = db.Column(db.String(255), nullable=False)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, filiaire, etablissement_id):
        self.name = name
        self.filiaire = filiaire
        self.etablissement_id = etablissement_id

    def __repr__(self):
        return f'<Filiaire {self.sigle} >'


class PubSchool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(255), nullable=True)
    text = db.Column(db.String(255), nullable=True)
    validate = db.Column(db.Boolean, nullable=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, filiaire, etablissement_id):
        self.name = name
        self.filiaire = filiaire
        self.etablissement_id = etablissement_id

    def __repr__(self):
        return f'<PubSchool {self.sigle} >'

class Messages(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    destinataire = db.Column(db.String(255), nullable=False)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, message, etablissement_id, destinataire):
        self.message = message
        self.etablissement_id = etablissement_id
        self.destinataire = destinataire

    def __repr__(self):
        return f'<Messages {self.sigle} >'

visitor_abonner = db.Table('visitor_abonner',
    db.Column('visitor_id', db.Integer, db.ForeignKey('visitor.id'), primary_key=True),
    db.Column('etablissement_id', db.Integer, db.ForeignKey('etablissement.id'), primary_key=True)
)

class Statistiques(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    click = db.Column(db.String(255), nullable=False)
    abonner = db.Column(db.String(255), nullable=False)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, click, password, tel, description):
        self.click = click
        self.password = password
        self.tel = tel
        self.description = description


    def __repr__(self):
        return f'<Statistiques {self.sigle} >'




class Visitor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    tel = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    visitor_abonner = db.relationship('Visitor', secondary=visitor_abonner, lazy='subquery',
                                      backref=db.backref('abonner', lazy=True))

    def __init__(self, username, tel, password, status):
        self.username = username
        self.tel = tel
        self.password = password
        self.status = status
        
        
class Sudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, password):
        self.name = name
        self.password = password
        
        
class PubEntreprise(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(255), nullable=True)
    validate = db.Column(db.Boolean, nullable=True)
    text = db.Column(db.String(255), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=False)


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, filiaire, etablissement_id):
        self.name = name
        self.filiaire = filiaire
        self.etablissement_id = etablissement_id

    def __repr__(self):
        return f'<PubSchool {self.sigle} >'


class Entreprise(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    tel = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activity = db.Column(db.String(80), nullable=False)
    pubSchool = db.relationship('PubSchool', backref="entreprise", lazy=True)

