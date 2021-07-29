from config import request, db, jsonify, app, api, Resource, bcrypt, abort
from Model.Model import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


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


@app.route("/add-school", methods=['POST'])
def addUser():
    name = request.json['name']
    sigle = request.json['sigle']
    logo = request.json['logo']
    position = request.json['position']
    status = request.json['status']
    multiple = request.json['multiple']
    type = request.json['type']
    profil = request.json['profil']
    description = request.json['description']
    pro = request.json['pro']
    stat = request.json['stat']
    create_at = request.json['create_at']
    outro = request.json['outro']
    tel = request.json['tel']
    pas = request.json['newpassword']
    sec_pas = bcrypt.generate_password_hash(pas)
    stat = request.json['status']

    new_user = User(username, tel, sec_pas, status, position)
    verif_user_exist = User.query.filter_by(tel=tel, username=username).first()
    if verif_user_exist is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=entrepise_schema.dump(new_user))
    return {"id": new_user.id, "username": new_user.username, "token": access_token}, 200















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
