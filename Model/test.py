from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import secret

CONNECT = f"mysql+pymysql://{secret.dbuser}:{secret.dbpass}@{secret.dbhost}/{secret.dbname}"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECT
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET-KEY"
db = SQLAlchemy(app)
ma = Marshmallow(app)


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
    pub = db.relationship('Pub', backref="etablissement", lazy=True)



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


class EtablissementSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Etablissement

    id = ma.auto_field()
    name = ma.auto_field()
    position = ma.auto_field()
    password = ma.auto_field()
    tel = ma.auto_field()
    description = ma.auto_field()
    sigle = ma.auto_field()
    logo = ma.auto_field()
    profil = ma.auto_field()
    pro = ma.auto_field()


class Entreprise(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    tel = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activity = db.Column(db.String(80), nullable=False)
    pub = db.relationship('Pub', backref="entreprise", lazy=True)

    def __init__(self, username, tel, password, activity):
        self.username = username
        self.tel = tel
        self.password = password,
        self.activity = activity,


class EntrepriseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entreprise

    username = ma.auto_field()
    tel = ma.auto_field()
    password = ma.auto_field()
    activity = ma.auto_field()
    include_fk = True


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


class Pub(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(255), nullable=True)
    text = db.Column(db.String(255), nullable=True)
    validate = db.Column(db.Boolean, nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=True)


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
    db.Column('etablissement_id', db.Integer, db.ForeignKey('etablissement.id'), primary_key=True),
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

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Statistiques {self.username} >'


class VisitorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Entreprise

    id = ma.auto_field()
    username = ma.auto_field()
    tel = ma.auto_field()
    password = ma.auto_field()
    status = ma.auto_field()
    include_fk = True


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













class UserRessource(Resource):
    def post(self, id):
        username = request.json['username']
        p = request.json['password']
        user = User.query.get(id)
        if bcrypt.check_password_hash(user.password, p) is True:
            access_token = create_access_token(identity=user_schema.dump(user))
            return access_token, 200
        return {"message": "cette utilistauer n'existe pas"}, 500

    @jwt_required()
    def get(self):
        res = get_jwt_identity()
        return res, 200

    @jwt_required()
    def put(self):
        user = get_jwt_identity()
        username = request.json['username']
        tel = request.json['tel']
        pas = request.json['oldPassword']
        new_pas = request.json['password']
        stat = request.json['status']

        if bcrypt.check_password_hash(user.password, pas) is True:
            user.username = username
            user.password = bcrypt.generate_password_hash(new_pas)
            user.tel = tel
            user.stat = stat
            db.session.commit()


api.add_resource(UserRessource, "/users/<int:id>")


@app.route("/add-user", methods=['POST'])
def addUser():
    username = request.json['username']
    tel = request.json['tel']
    pas = request.json['password']
    sec_pas = bcrypt.generate_password_hash(pas)
    stat = request.json['status']

    new_user = User(username, tel, sec_pas, stat)
    verif_user_exist = User.query.filter_by(tel=tel, username=username).first()
    if verif_user_exist is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=id)
    return jsonify(access_token=access_token), 200















