#coding:utf-8
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from config import request, db, jsonify, app, api, Resource, bcrypt, abort, os
from Model.Model import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from base64 import b64encode
import base64
from werkzeug.utils import secure_filename

from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

UPLOAD_FOLDER = os.pardir + '/front/public'
ALLOWED_EXTENSIONS = ['webp', 'svg', 'png', 'jpg', 'jpeg']



#Tools






def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext in ALLOWED_EXTENSIONS or ext.upper() in ALLOWED_EXTENSIONS:
        return True
    else:
        print("retour pour tous ça")
        return False, 500


@app.route('/upload', methods=['POST'])
def fileUpload():
    image = request.files["file"]
    filename = secure_filename(image.filename)
    if filename in os.listdir():
        return jsonify(True), 200
    allowed_image(filename)
    image.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify(True), 200


@app.route('/upload', methods=['DELETE'])
def fileDelete():
    image = request.json["file"]
    print(os.path.join(UPLOAD_FOLDER, image))
    os.remove(os.path.join(UPLOAD_FOLDER, image))
    return jsonify(True), 200




#User Partie

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
            access_token = create_access_token(identity= res['id'])
            return {"id": res["id"], "username": res["username"], "token": access_token}, 200
    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/sudo", methods=['PUT'])
def putSudo():
    p = request.json['oldpassword']
    user = Sudo.query.get(1)
    print(user)
    new_pas = request.json['password']
   
    if bcrypt.check_password_hash(user.password, p) is True:
        print("ici")
        user.password = bcrypt.generate_password_hash(new_pas)
        db.session.commit()
        return {"msg": "fine"}, 200
        
    return {"message": "cette utilistauer n'existe pas"}, 500





@app.route("/sudo", methods=['POST'])
def postSudo():
    username = request.json['username']
    newp = request.json['password']
    users = Sudo.query.filter_by(name=username).all()
    result = sudos_schema.dump(users)

    for res in result:
        if bcrypt.check_password_hash(res["password"], newp) is True:
            access_token = create_access_token(identity= res['id'])
            return {"id": res["id"], "token": access_token}, 200
    return {"message": "cette utilistauer n'existe pas"}, 500




@app.route("/users", methods=['GET'])
def getUsers():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)


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

    access_token = create_access_token(identity= new_user.id)
    return {"id": new_user.id, "username": new_user.username, "token": access_token}, 200


@app.route("/add-sudo", methods=['POST'])
def addSudoUser():
    username = request.json['username']
    pas = request.json['password']
    sec_pas = bcrypt.generate_password_hash(pas)

    new_user = Sudo(username, sec_pas)
    verif_user_exist = Sudo.query.filter_by(name=username).first()
    if verif_user_exist is None:
        db.session.add(new_user)
        db.session.commit()
    else:
        abort(409, message="La ressource existe déja")

    access_token = create_access_token(identity=new_user.id)
    return {"id": new_user.id, "username": new_user.name, "token": access_token}, 200


#Entreprise Partie



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

    access_token = create_access_token(identity=new_user.id)
    return {"id": new_user.id, "username": new_user.username, "etoken": access_token}, 200


@app.route("/entreprises", methods=['GET'])
def get_entreprises():
    all_users = Entreprise.query.all()
    result = entreprises_schema.dump(all_users)

    return jsonify(result)






# School Partie





class SchoolRessource(Resource):
    def get(self, id):
        school = School.query.filter_by(id=id).first()
        result = school_schema.dump(school)
        return result,200

    def put(self, id):
        school = School.query.filter_by(id=id).first()
        name = request.json['name']
        sigle = request.json['sigle']
        logo = request.json['logo']
        profil = request.json['profil']
        status = request.json['status']
        multiple = request.json['multiple']
        description = request.json['description']
        positions = request.json['positions']
        types = request.json['type']
        outro = request.json['outro']
        tel = request.json['tel']


        school.name = name
        school.sigle = sigle
        school.logo = logo
        school.profil = profil
        school.status = status
        school.multiple = multiple
        
        school.description = str(description)
        school.outro = str(outro)
        
        school.tel = tel
        positionsQuery = Position.query.filter_by(school_id = id).all()
        typesQuery = Types.query.filter_by(school_id = id).all()

       


        
        for p in positions:
            school.position.append(Position(p["value"]))
        for t in types:
            school.types.append(Types(t["value"]))
        
        for p in positionsQuery:
            db.session.delete(p)
        for t in typesQuery:
            db.session.delete(t)

        db.session.commit()
       

        return True, 200


api.add_resource(SchoolRessource, "/schools/<int:id>")



@app.route("/addStatSchool/<int:id>", methods=['PUT'])
def addStatSchool(id):
    school = School.query.get(id)
    now = int(school.stat) 
    school.stat = now + 1
    db.session.commit()

    return {"msg": True}, 200


@app.route("/ToggleStatusSchool/<int:id>", methods=['PUT'])
def ToggleStatusSchool(id):
    school = School.query.get(id)
    school.pro = True
    school.demande = False
    db.session.commit()

    return {"msg": True}, 200


@app.route("/TogglevStatusSchool/<int:id>", methods=['PUT'])
def ToggleStatusvSchool(id):
    school = School.query.get(id)
    school.pro = not school.pro
    school.demande = False
    db.session.commit()

    return {"msg": True}, 200

@app.route("/DelStatusSchool/<int:id>", methods=['PUT'])
def DelToggleStatusSchool(id):
    school = School.query.get(id)
    school.demande = False
    db.session.commit()

    return {"msg": True}, 200

@app.route("/schools", methods=['GET'])
def get_schools():
    all_users = School.query.all()
    result = schools_schema.dump(all_users)

    return jsonify(result)

@app.route("/schools/get/<slug>", methods=['GET'])
def get_slug_schools(slug):
    all_users = School.query.filter_by(sigle = slug).first()
    result = school_schema.dump(all_users)

    if result["id"] is None:
        return False,500

    return jsonify(result)




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

    access_token = create_access_token(identity=new_school.id)
   
  
    return {"id": new_school.id, "sigle": new_school.sigle, "token": access_token}, 200


@app.route("/school", methods=['POST'])
def postSchool():
    username = request.json['username']
    username = username.upper()
    p = request.json['password']
    school = School.query.filter_by(sigle=username).all()
    result = schools_schema.dump(school)
    for res in result:
        if bcrypt.check_password_hash(res["password"], p) is True:
            access_token = create_access_token(
                identity = res["id"])
            return {"id": res["id"], "school": res["sigle"], "schoolToken": access_token}, 200
    return {"message": "cette école n'existe pas"}, 500



# SchoolPro

@app.route("/secschools/<int:id>", methods=["GET"])
@jwt_required()
def getSecSchool(id):
    school = School.query.filter_by(id=id).first()
    result = school_schema.dump(school)
    user = get_jwt_identity()
    if user != result["id"]:
        return {"msg": "Vous n'avez pas le droit à ce contenu"}, 401
                     
    return result, 200





# > Filiaires

@app.route("/filieres", methods = ["GET"])
def getFilieres():
    all_users = Filiaire.query.all()
    result = filiaires_schema.dump(all_users)

    return jsonify(result), 200


@app.route("/custom-filieres/<int:id>", methods = ["GET"])
def getCustomFilieres(id):
    all_users = Filiaire.query.filter_by(school_id = id).all()
    result = filiaires_schema.dump(all_users)

    return jsonify(result), 200



@app.route("/demande/<int:id>", methods = ["PUT"])
def getCustomDemande(id):
    school = School.query.filter_by(id = id).first()
    school.demande = not school.demande
    db.session.commit()

    return {}, 200


@app.route("/add-filiaire", methods=['POST'])
def addFiliaire():
    fil = request.json['fil']
    school_id = request.json['schoolId']
    school_id = int(school_id)
    school = School.query.filter_by(id=school_id).first()
    fil_exist = Filiaire.query.filter_by(name=fil).first()


    if fil_exist is None:     
        new_fil = Filiaire(fil)
        school.filiaire.append(new_fil)
        db.session.add(new_fil)
        db.session.commit()
        return {"id": new_fil.id}, 200
    else:
        abort(409, message="La ressource existe déja")

       

@app.route("/message", methods=['POST'])
def addMesasage():
    userId = int(request.json['userId'])
    schoolId = int(request.json['schoolId'])
    message = request.json['message']

    school = School.query.filter_by(id=schoolId).first()
    user = User.query.filter_by(id=userId).first()

    mes = SchoolMessage(message=message)

    with db.session.no_autoflush:
        school.message.append(mes)
        user.schoolMessage.append(mes)
    db.session.add(mes)
    db.session.commit()
    return {"ms": True},200
 

@app.route("/message/<int:id>", methods=['GET'])
def getMesasage(id):
    
    school = School.query.filter_by(id=id).first()

    mes = SchoolMessage.query.order_by(SchoolMessage.id.desc()).filter_by(school_id = school.id).all()
    result = schools_message_schema.dump(mes)
    tab = []
    for r in result:
        
        tab.append({"user": user_schema.dump(User.query.get(r["user_id"])), "message": r["message"]})
        

  
    return jsonify(tab), 200
    

    


class FiliaireRessource(Resource):

  @jwt_required()
  def get(self, id):
      school = Filiaire.query.filter_by(id=id).first()
      result = filiaire_schema.dump(school)
      return result, 200
  
  @jwt_required()
  def put(self, id):
      user = Filiaire.query.get(id)
      fil = request.json['name']
      user.name = fil
      db.session.commit()
      return True, 200

      



  @jwt_required()
  def delete(self, id):
      filiaire = Filiaire.query.get(id)
      spe = Speciality.query.filter_by(filiaire_id=id).all()
      result = specialities_schema.dump(spe)
      if result != []:
          for s in spe:
            db.session.delete(s)
          db.session.delete(filiaire)
          db.session.commit()
          return jsonify(result)    
      else:
          db.session.delete(filiaire)
          db.session.commit()
     
api.add_resource(FiliaireRessource, "/filieres/<int:id>")


# > Types

@app.route("/types", methods=["GET"])
def getTypes():
    all_users = Types.query.all()
    result = types_schema.dump(all_users)

    return jsonify(result)


@app.route("/custom-types/<int:id>", methods=["GET"])
def getCustomTypes(id):
    all_users = Types.query.filter_by(school_id = id).all()
    result = types_schema.dump(all_users)

    return jsonify(result)


# > Positions

@app.route("/positions", methods=["GET"])
def getPositions():
    all_users = Position.query.all()
    result = positions_schema.dump(all_users)
    

    return jsonify(result)


@app.route("/custom-positions/<int:id>", methods=["GET"])
def getCustomPositions(id):
    all_users = Position.query.filter_by(school_id = id).all()
    result = positions_schema.dump(all_users)

    return jsonify(result)

# > Speciality




@app.route("/specialities", methods=["GET"])
def getSpecialities():
    all_users = Speciality.query.all()
    result = specialities_schema.dump(all_users)
    

    return jsonify(result)



@app.route("/custom-specialities/<int:id>", methods=["GET"])
def getCustomSpecialities(id):
    all_users = Speciality.query.filter_by(school_id=id).all()
    result = specialities_schema.dump(all_users)
    

    return jsonify(result)




@jwt_required()
@app.route("/add-speciality", methods=['POST'])
def addSpeciality():
    name = request.json['name']
    school_id = request.json['schoolId']
    fil = request.json['fil']
    prix = request.json['prix']
    school_id = int(school_id)
    school = School.query.filter_by(id=school_id).first()
    filiaire = Filiaire.query.filter_by(name=fil).first()
    spe_exist = Speciality.query.filter_by(name=name).first()


    if spe_exist is None:     
        new_spe = Speciality(name, prix)
        with db.session.no_autoflush:
            filiaire.speciality.append(new_spe)
            school.speciality.append(new_spe)
        db.session.add(new_spe)
        db.session.commit()
        
        return {"id": new_spe.id}, 200
    else:
        abort(409, message="La ressource existe déja")









class SpecialityRessource(Resource):

  @jwt_required()
  def get(self, id):
      school = Speciality.query.filter_by(id=id).first()
      result = speciality_schema.dump(school)
      return result, 200

  @jwt_required()
  def put(self, id):
      user = Speciality.query.get(id)
      name = request.json['name']
      price = request.json['prix']
      fil = request.json['fil']
      user.name = name
      user.fil = fil
      user.price = price
      filiaire = Filiaire.query.filter_by(name=fil).first()
      print(filiaire)
      if filiaire == None:
          db.session.commit()
          return True,200
      filiaire.speciality.append(user)
      db.session.commit()
      return True, 200





  @jwt_required()
  def delete(self, id):
      filiaire = Speciality.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()


api.add_resource(SpecialityRessource, "/speciality/<int:id>")

#Commentaires

@jwt_required()
@app.route("/abonnement", methods=['POST'])
def addCommentaire():
    school_id = int(request.json['schoolId'])
    user_id = int(request.json['userId'])
    school = School.query.filter_by(id=school_id).first()
    user = User.query.filter_by(id=user_id).first()
    
    
    school.abonnement.append(user)

    db.session.commit()

    return {"m": True}, 200

        
@app.route("/abonnement/<int:id>", methods=['GET'])
def getUserSchool(id):
    
    school = School.query.filter_by(id=id).first()
    result = []
    for user in school.abonnement:
        result.append(user.id)

    return {"abo": result}


@app.route("/schoolAbonnement/<int:id>", methods=['GET'])
def getUserAboSchool(id):
    
    school = School.query.filter_by(id=id).first()
    result = []
    for user in school.abonnement:
        result.append(user_schema.dump(user))

    return jsonify(result)




# Run server
if __name__ == "__main__":
    app.run(debug=True)
