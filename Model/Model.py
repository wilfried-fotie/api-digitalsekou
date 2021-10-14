#coding:utf-8
from config import db, ma, bcrypt
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
    schoolMessage = db.relationship(
        'SchoolMessage', backref="user", lazy="select")
    entrepriseMessage = db.relationship(
        'EntrepriseMessage', backref="user", lazy="select")
    abonnement = db.relationship('School', secondary=abonnement, lazy='select',cascade='all, delete-orphan', single_parent=True, backref='abonnement')

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
    site = db.Column(db.Boolean, nullable=False, default=False)
    demande = db.Column(db.Boolean, nullable=False, default=False)
    pro = db.Column(db.Boolean, nullable=False, default=False)
    pub = db.relationship('Pub', backref="entreprise", lazy=True)
    offer = db.relationship('Offer', backref="entreprise", lazy=True)
    addPost = db.relationship('AddPost', backref="entreprise", lazy=True)
    addProduct = db.relationship('AddProduct', backref="entreprise", lazy=True)
    entrepriseSite = db.relationship(
        'SiteEntreprise', backref="entreprise", lazy=True)
    position = db.relationship(
        'PositionEntreprise', backref='school', lazy="select")

    def __init__(self, username, tel, password, site=None, demande=None, pro=None):
        self.username = username
        self.tel = tel
        self.password = password
        self.site = site
        self.demande = demande
        self.pro = pro


class EntrepriseSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "username", "tel", "site","password","demande","pro","activity")


# init schema
entrepise_schema = EntrepriseSchema()
entreprises_schema = EntrepriseSchema(many=True)


class Pub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    available = db.Column(db.DateTime, nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=False)
    proprio = db.Column(db.Boolean, nullable=True)
    demande = db.Column(db.Boolean, nullable=False,default=True)
    stat = db.Column(db.Integer, nullable=False,default=0)
    days = db.Column(db.DateTime, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

    def __init__(self, media, available,  proprio,  days,name, stat=None,valid=None,demande=None):
        self.media = media
        self.available = available
        self.valid = valid
        self.demande = demande
        self.proprio = proprio
        self.stat = stat
        self.days = days
        self.name = name


class PubSchema(ma.Schema):
    class Meta:
        fields = ("id","media", "create_at", "valid", "proprio",
                  "available", "demande", "name", "days", "stat","entreprise_id")


pubSchema = PubSchema()
pubsSchema = PubSchema(many=True)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    valid = db.Column(db.Boolean, nullable=False, default=False)
    demande = db.Column(db.Boolean, nullable=False,default=True)
    proprio = db.Column(db.Boolean, nullable=True)
    stat = db.Column(db.Integer, nullable=False,default=0)
    expire = db.Column(db.DateTime, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

    def __init__(self, logo,  proprio, title, url,tel, content, expire, stat=None, create_at=None, valid=None, demande=None):
        self.logo = logo
        self.create_at = create_at
        self.valid = valid
        self.demande = demande
        self.proprio = proprio
        self.title = title
        self.tel = tel
        self.content = content
        self.stat = stat
        self.expire = expire
        self.url = url


class OfferSchema(ma.Schema):
    class Meta:
        fields = ("id", "logo", "valid", "proprio", "title", "tel",
                  "demande", "url", "content", "expire", "stat", "create_at","entreprise_id")


offerSchema = OfferSchema()
offersSchema = OfferSchema(many=True)

class Speciality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    who = db.Column(db.String(255), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)

    def __init__(self, name, price, description, who, school_id=None):
        self.name = name
        self.price = price
        self.description = description
        self.school_id = school_id
        self.who = who


# Product Schema
class SpecialitySchema(ma.Schema):
    class Meta:
        fields = (
            "id", "name","price","description","who", "school_id")


# init schema
speciality_schema = SpecialitySchema()
specialities_schema = SpecialitySchema(many=True)


class PositionEntreprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    entreprise_id = db.Column(db.Integer, db.ForeignKey(
        "entreprise.id"), nullable=False)

    def __init__(self,position,entreprise_id=None):
        self.position = position
        self.entreprise_id = entreprise_id


class PositionEntrepriseSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "position", "entrerise_id")


position_entreprise_schema = PositionEntrepriseSchema()
positions_entreprise_schema = PositionEntrepriseSchema(many=True)


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
    message = db.Column(db.Text, nullable=False)
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
    disposition = db.Column(db.Integer,nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    position = db.relationship('Position', backref='school', lazy="select")
    types = db.relationship('Types', backref='school', lazy="select")
    speciality = db.relationship('Speciality', backref='school', lazy="select")
    message = db.relationship(
        'SchoolMessage', backref="school", lazy="select")
    pub = db.relationship('Pub', backref="school", lazy="select")
    offer = db.relationship('Offer', backref="school", lazy="select")
    addPost = db.relationship('AddPost', backref="school", lazy=True)

    def __init__(self, name, password, tel, description, disposition, sigle, logo, profil, multiple, outro,status,demande=None,pro=None,stat=None):
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
        self.disposition = disposition
        self.stat = stat

    def __repr__(self):
        return f"<School name={self.sigle} logo={self.logo}>"


# Product Schema
class SchoolSchema(ma.Schema):
    class Meta:
        fields = (
           "id", "name", "password", "tel", "description","disposition", "sigle", "logo", "profil", "pro","create_at","demande","stat","status", "multiple",
            "outro")



class EntrepriseMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    site_entreprise_id = db.Column(db.Integer, db.ForeignKey(
        "site_entreprise.id"), nullable=False)

    def __init__(self, message):
        self.message = message


class EntrepriseMessageSchema(ma.Schema):
    class Meta:
        fields = ("id", "message", "user_id")


entreprise_message_schema = EntrepriseMessageSchema()
entreprises_message_schema = EntrepriseMessageSchema(many=True)


class SiteEntreprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stat = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    tel = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    profil = db.Column(db.String(255), nullable=False)
    site = db.Column(db.String(50), nullable=True)
    disposition = db.Column(db.Integer,nullable=False)
    online = db.Column(db.Boolean, nullable=False, default=False)
    offline = db.Column(db.Boolean, nullable=False, default=False)
    pres = db.Column(db.Boolean, nullable=False)
    prod = db.Column(db.Boolean, nullable=False)
    description_position = db.Column(db.Text, nullable=True)
    outro = db.Column(db.Text, nullable=False)
    # pro = db.Column(db.Boolean, nullable=False, default=False)
    # demande = db.Column(db.Boolean, nullable=False, default=False)
    
    message = db.relationship(
        'EntrepriseMessage', backref="site_entreprise", lazy="select")

    create_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow())
    entreprise_id = db.Column(
        db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

   
    
    def __init__(self, name,  tel, logo, site, profil, activity, outro,description_position, disposition, offline,online,pres,prod, demande=None, pro=None, stat=None):
        self.name = name
        self.tel = tel
        self.logo = logo
        self.pres = pres
        self.prod = prod
        self.activity = activity
        self.offline = offline
        self.site = site
        self.online = online
        self.profil = profil
        self.outro = outro
        self.description_position = description_position
        self.pro = pro
        self.demande = demande
        self.stat = stat
        self.disposition = disposition

    def __repr__(self):
        return f"<School name={self.name} logo={self.logo}>"


# Product Schema
class SiteEntrepriseSchema(ma.Schema):
    class Meta:
        fields = (
           "id", "name", "tel","description_position" , "disposition", "site", "pres","prod","activity", "logo", "profil", "create_at","stat","offline","online",
            "outro","entreprise_id")


siteEntreprise = SiteEntrepriseSchema()
sitesEntreprise = SiteEntrepriseSchema(many=True)



#Creation du model addPost


class AddPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    disposition = db.Column(db.Integer,nullable=False)
    proprio = db.Column(db.Boolean, nullable=False)
    school_id = db.Column(
        db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(
        db.Integer, db.ForeignKey('entreprise.id'), nullable=True)



    def __init__(self,image,description,disposition,name,proprio):
        self.image = image
        self.description = description
        self.disposition = disposition
        self.proprio = proprio
        self.name = name

class AddPostSchema(ma.Schema):
    class Meta():
        fields = ("id","image","name","description","disposition","proprio","school_id","entreprise_id")


addPostSchema = AddPostSchema()
addPostsSchema = AddPostSchema(many=True)


#creation du model addProduct


class AddProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    proprio = db.Column(db.Boolean, nullable=True)
    school_id = db.Column(
        db.Integer, db.ForeignKey('school.id'), nullable=True)
    entreprise_id = db.Column(
        db.Integer, db.ForeignKey('entreprise.id'), nullable=True)

    def __init__(self,image,price,proprio,name):
        self.image = image
        self.price = price
        self.proprio = proprio
        self.name = name


class AddpProductSchema(ma.Schema):
    class Meta():
        fields = ("id","image","price","name","proprio","entreprise_id")


addProductSchema = AddpProductSchema()
addProductsSchema = AddpProductSchema(many=True)



# init schema

school_schema = SchoolSchema()
schools_schema = SchoolSchema(many=True)


class Sudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False, default=bcrypt.generate_password_hash("12345678"))

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
