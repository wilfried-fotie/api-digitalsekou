from config import request, db, jsonify, app, api, Resource, bcrypt, abort, os
from Model.Model import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from base64 import b64encode
import base64
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.pardir + '/front/public'
ALLOWED_EXTENSIONS = ['webp', 'svg', 'png', 'jpg', 'jpeg']


class UserRessource(Resource):

    @jwt_required()
    def get(self, id):
        user = User.query.get(id)
        result = user_schema.dump(user)

        return jsonify(result)

    @jwt_required()
    def put(self, id):
        user = User.query.get(id)
        username = request.json['username']
        tel = request.json['tel']
        pas = request.json['oldpassword']
        new_pas = request.json['newpassword']
        status = request.json['status']

        if bcrypt.check_password_hash(user.password, pas) is True:
            user.username = username
            if new_pas == "":
                pass
            else:
                user.password = bcrypt.generate_password_hash(new_pas)
            user.tel = tel
            user.status = status
            db.session.commit()
            return True, 200
        return "error", 500


api.add_resource(UserRessource, "/users/<int:id>")


@app.route("/user", methods=['POST'])
def postUser():
    username = request.json['username']
    p = request.json['password']
    users = User.query.filter_by(username=username).all()
    result = users_schema.dump(users)
    for res in result:
        if bcrypt.check_password_hash(res["password"], p) is True:
            access_token = create_access_token(identity=user_schema.dump(res))
            return {"id": res["id"], "username": res["username"], "token": access_token}, 200
    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/add-user", methods=['POST'])
def addUser():
    username = request.json['username']
    tel = request.json['tel']
    pas = request.json['newpassword']
    sec_pas = bcrypt.generate_password_hash(pas)
    stat = request.json['status']

    new_user = User(username, tel, sec_pas, stat)
    verif_user_exist = User.query.filter_by(tel=tel, username=username).first()
    if verif_user_exist is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=entrepise_schema.dump(new_user))
    return {"id": new_user.id, "username": new_user.username, "token": access_token}, 200





class SchoolRessource(Resource):

    
    def get(self, id):
        user = User.query.get(id)
        result = user_schema.dump(user)

        return jsonify(result)

    @jwt_required
    def put(self, id):
        user = User.query.get(id)
        name = request.json['name']
        tel = request.json['tel']
        pas = request.json['oldpassword']
        new_pas = request.json['newpassword']
        status = request.json['status']

        if bcrypt.check_password_hash(user.password, pas) is True:
            user.username = name
            if new_pas == "":
                pass
            else:
                user.password = bcrypt.generate_password_hash(new_pas)
            user.tel = tel
            user.status = status
            db.session.commit()
            return True, 200

        return "error", 500


def allowed_image(filename):

    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext in ALLOWED_EXTENSIONS or ext.upper() in ALLOWED_EXTENSIONS :
        return True
    else: 
        print("retour pour tous ça")
        return False, 500


@app.route('/upload', methods=['POST'])
def fileUpload():
    image = request.files["file"]
    filename = secure_filename(image.filename)
    allowed_image(filename)
    image.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify(True), 200


@app.route("/add-school", methods=['POST'])
def addSchool():
    
    name = request.json['name']
    sigle = request.json['sigle']
    logo = request.json['logoName']
    status = request.json['status']
    multiple = request.json['multiple']
    profil = request.json['profilName']
    description = request.json['description']
    outro = request.json['outro']
    tel = request.json['tel']
    pas = request.json['password']
    pas = bcrypt.generate_password_hash(pas)
    position = request.json['position'] 
    types = request.json['type']

    new_school = School(name=name, password=pas, tel=tel, description=description, sigle=sigle,
                        logo=logo, profil=profil, multiple=multiple, outro=outro, status=status)

    verif_user_exist = School.query.filter_by(
        tel=tel, name=name, sigle=sigle).first()
    if verif_user_exist is None:

        for type in types:
            new_type = Types(type["value"])
            db.session.add(new_type)
            
            new_school.types.append(new_type)

        for posi in position:
            new_position = Position(posi["value"])
            db.session.add(new_position)

            new_school.position.append(new_position)
        
        db.session.add(new_school)
    
        db.session.commit()
    
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=school_schema.dump(new_school))
    return {"id": new_school.id, "sigle": new_school.sigle, "token": access_token}, 200


@app.route("/school", methods=['POST'])
def postSchool():
    username = request.json['username']
    username = username.upper()
    print("-----------------------------------------------------" + username)
    p = request.json['password']
    school = School.query.filter_by(sigle=username).all()
    result = schools_schema.dump(school)
    for res in result:
        if bcrypt.check_password_hash(res["password"], p) is True:
            access_token = create_access_token(identity=school_schema.dump(res))
            return {"id": res["id"], "school": res["sigle"], "schoolToken": access_token}, 200
    return {"message": "cette école n'existe pas"}, 500














class EntrepriseRessource(Resource):

    @jwt_required()
    def get(self, id):
        user = Entreprise.query.get(id)
        result = entrepise_schema.dump(user)

        return jsonify(result)

    @jwt_required()
    def put(self, id):
        user = Entreprise.query.get(id)
        username = request.json['username']
        tel = request.json['tel']
        pas = request.json['oldpassword']
        new_pas = request.json['password']
        activity = request.json['activity']

        if bcrypt.check_password_hash(user.password, pas) is True:
            user.username = username

            if new_pas is None:
                user.password = bcrypt.generate_password_hash(pas)
            else:
                user.password = bcrypt.generate_password_hash(new_pas)
            user.tel = tel
            user.activity = activity
            db.session.commit()
            return True, 200
        else:
            return "error", 500


api.add_resource(EntrepriseRessource, "/entreprises/<int:id>")


@app.route("/entreprise", methods=['POST'])
def postEntreprise():
    username = request.json['username']
    p = request.json['password']
    users = Entreprise.query.filter_by(username=username).all()
    result = entreprises_schema.dump(users)
    for res in result:
        if bcrypt.check_password_hash(res["password"], p) is True:
            access_token = create_access_token(identity=entrepise_schema.dump(res))
            return {"id": res["id"], "username": res["username"], "etoken": access_token}, 200
    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/add-entreprise", methods=['POST'])
def addEntreprise():
    username = request.json['username']
    tel = request.json['tel']
    pas = request.json['newpassword']
    sec_pas = bcrypt.generate_password_hash(pas)
    activity = request.json['activity']

    new_user = Entreprise(username, tel, sec_pas, activity)
    verif_user_exist = Entreprise.query.filter_by(tel=tel, username=username).first()
    if verif_user_exist is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=entrepise_schema.dump(new_user))
    return {"id": new_user.id, "username": new_user.username, "etoken": access_token}, 200


@app.route("/entreprises", methods=['GET'])
def get_entreprises():
    all_users = Entreprise.query.all()
    result = entreprises_schema.dump(all_users)

    return jsonify(result)


@app.route("/users", methods=['GET'])
def getUsers():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)


class SchoolRessource(Resource):
    def get(self, id):
        school = School.query.filter_by(id=id).first()
        result = schools_schema.dump(school)
        return jsonify(result)


api.add_resource(SchoolRessource, "/schools/<int:id>")


# Get all users
@app.route("/schools", methods=['GET'])
def get_schools():
    all_users = School.query.all()
    result = schools_schema.dump(all_users)

    return jsonify(result)


# Run server
if __name__ == "__main__":
    app.run(debug=True)
