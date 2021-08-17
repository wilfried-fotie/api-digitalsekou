from config import db, ma
from datetime import datetime

# User class model
abonnement = db.Table('abonnement',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                      db.Column('school_id', db.Integer, db.ForeignKey('school.id'), nullable=False),
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    tel = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(255))
    schoolMessage = db.relationship('SchoolMessage', backref="user", lazy="select")
    abonnement = db.relationship('School', secondary=abonnement, lazy='select', backref='abonnement')

    def __init__(self, username, tel, password, status):
        self.username = username
        self.tel = tel
        self.password = password
        self.status = status

    def __repr__(self):
        return f"<User username={self.username}>"


# Product Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "tel", "password", "status")


# init schema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Entreprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    tel = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activity = db.Column(db.String(255), nullable=False)
    pub = db.relationship('Pub', backref="entreprise", lazy=True)

    def __init__(self, username, tel, password, activity):
        self.username = username
        self.tel = tel
        self.password = password,
        self.activity = activity,


class EntrepriseSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "username", "password", "tel", "password", "activity")


# init schema
entrepise_schema = EntrepriseSchema()
entreprises_schema = EntrepriseSchema(many=True)


class Pub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    proprio = db.Column(db.Boolean, nullable=True)
    stat = db.Column(db.Integer, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

    def __init__(self, media, create_at, valid, proprio, stat):
        self.media = media
        self.create_at = create_at
        self.valid = valid
        self.proprio = proprio
        self.stat = stat


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    proprio = db.Column(db.Boolean, nullable=True)
    stat = db.Column(db.Integer, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

    def __init__(self, logo, create_at, valid, proprio, stat, title, tel, content):
        self.logo = logo
        self.create_at = create_at
        self.valid = valid
        self.proprio = proprio
        self.title = title
        self.tel = tel
        self.content = content
        self.stat = stat


class Filiaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False,unique=True)
    speciality = db.relationship('Speciality', backref="filiaire", lazy="select")
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)

    def __init__(self, name,  school_id=None):
        self.name = name
        self.school_id = school_id


# Product Schema
class FiliaireSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "name","school_id")


# init schema
filiaire_schema = FiliaireSchema()
filiaires_schema = FiliaireSchema(many=True)

class Speciality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    filiaire_id = db.Column(db.Integer, db.ForeignKey(
        "filiaire.id"), nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)

    def __init__(self, name,price,filiaire_id=None,school_id=None):
        self.name = name
        self.price = price
        self.filiaire_id = filiaire_id
        self.school_id = school_id


# Product Schema
class SpecialitySchema(ma.Schema):
    class Meta:
        fields = (
            "id", "name","price","filiaire_id","school_id")


# init schema
speciality_schema = SpecialitySchema()
specialities_schema = SpecialitySchema(many=True)



class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey(
        "school.id"), nullable=False)

    def __init__(self,position,school_id=None):
        self.position = position
        self.school_id = school_id


class PositionSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "position", "school_id")


position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)


class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    types = db.Column(db.String(100), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey(
        "school.id"), nullable=False)

    def __init__(self, types):
        self.types = types


class TypesSchema(ma.Schema):
    class Meta:
        fields = ("id", "types","school_id")


type_schema = TypesSchema()
types_schema = TypesSchema(many=True)



class SchoolMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)

    def __init__(self, message):
        self.message = message


class SchoolMessageSchema(ma.Schema):
    class Meta:
        fields = ("id", "message", "user_id")


school_message_schema = SchoolMessageSchema()
schools_message_schema = SchoolMessageSchema(many=True)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stat = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    profil = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    outro = db.Column(db.Text, nullable=False)
    sigle = db.Column(db.String(40), nullable=False)
    pro = db.Column(db.Boolean, nullable=False, default=False)
    demande = db.Column(db.Boolean, nullable=False, default=False)
    multiple = db.Column(db.String(40), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    filiaire = db.relationship('Filiaire', backref='school', lazy="select")
    position = db.relationship('Position', backref='school', lazy="select")
    types = db.relationship('Types', backref='school', lazy="select")
    speciality = db.relationship('Speciality', backref='school', lazy="select")
    pub = db.relationship('Pub', backref="school", lazy="select")
    offer = db.relationship('Offer', backref="school", lazy="select")
    message = db.relationship('SchoolMessage', backref="school", lazy="select")

    def __init__(self, name, password, tel, description, sigle, logo, profil, multiple, outro,status,demande=None,pro=None,stat=None):
        self.name = name
        self.password = password
        self.tel = tel
        self.description = description
        self.sigle = sigle
        self.logo = logo
        self.status = status
        self.profil = profil
        self.outro = outro
        self.multiple = multiple
        self.pro = pro
        self.demande = demande
        self.stat = stat

    def __repr__(self):
        return f"<School name={self.sigle} logo={self.logo}>"


# Product Schema
class SchoolSchema(ma.Schema):
    class Meta:
        fields = (
           "id", "name", "password", "tel", "description", "sigle", "logo", "profil", "pro","create_at","demande","stat","status", "multiple",
            "outro")


# init schema

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)


class Sudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def __init__(self, name, password):
        self.name = name
        self.password = password


class SudoSchema(ma.Schema):
    class Meta:
        fields = ("id", "name","password")


sudo_schema = SudoSchema()
sudos_schema = SudoSchema(many=True)

# db.drop_all()
# db.create_all()
