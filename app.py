#coding:utf-8
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from re import UNICODE
from config import request, db, jsonify, app, api, Resource, bcrypt, abort, os
from Model.Model import *
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from base64 import b64encode
import base64
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies


UPLOAD_FOLDER = os.pardir + '/front/public/Images'
ALLOWED_EXTENSIONS = ['webp', 'svg',"SVG", 'png', 'jpg', 'jpeg',"JPG","PNG","JPEG","mp4","MP4"]



#Tools

def verif_date(date):
    if int(date[0]) >= int(datetime.today().year):
        
        if int(date[1]) >= int(datetime.today().month) or int(date[0]) > int(datetime.today().year):
            if int(date[2].split("T")[0]) >= int(datetime.today().day) or int(date[1]) > int(datetime.today().month) :
                return True
            else:
                return False
            
        else:
            
            return False
    else: 
        return False





def reverse_verif_date(date):
    if int(date[0]) <= int(datetime.today().year):
        
        if int(date[1]) <= int(datetime.today().month) and int(date[0]) <= int(datetime.today().year):
            if int(date[2].split("T")[0]) <= int(datetime.today().day) or int(date[1]) < int(datetime.today().month):
                return True
            else:
                return False
            
        else:
            
            return False
    else: 
        return False

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

    
    if allowed_image(filename):

        image.save(os.path.join(UPLOAD_FOLDER, filename))
        # s3.upload_file(Filename=filename, Bucket="digitalsekou", Key=filename)
    return jsonify(True), 200



@app.route('/upload/<image>', methods=['DELETE'])
def fileDelete(image):
    delete = os.path.join(UPLOAD_FOLDER, image)
    print(delete)
    os.remove(delete)

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
        username = request.json['username'].lower().replace(" ", "-")
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
    @jwt_required()
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()





api.add_resource(UserRessource, "/users/<int:id>")


@app.route("/user", methods=['POST'])
def postUser():
    username = request.json['username']
    p = request.json['password']
    users = User.query.filter_by(
        username=username.lower()).all()
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
        return {"msg": "fin"}, 200
        
    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/entreprise-pass", methods=['PUT'])
def putEntreprisePass():
    p = request.json['oldpassword']
    id = request.json['id']
    user = Entreprise.query.get(id)
    new_pas = request.json['password']
   
    if bcrypt.check_password_hash(user.password, p) is True:
        user.password = bcrypt.generate_password_hash(new_pas)
        db.session.commit()
        return {"msg": "fin"}, 200
        
    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/school-change-pass", methods=['PUT'])
def putSchoolPass():
    p = request.json['oldpassword']
    id = request.json['id']
    user = School.query.get(id)
    new_pas = request.json['password']

    if bcrypt.check_password_hash(user.password, p) is True:
        user.password = bcrypt.generate_password_hash(new_pas)
        db.session.commit()
        return {"msg": "fin"}, 200

    return {"message": "cette utilistauer n'existe pas"}, 500


@app.route("/sudoeur", methods=['GET'])
def postSudoBiz():
   
    users = Sudo("admin",bcrypt.generate_password_hash("12345678"))
    db.session.add(users)
    db.session.commit()
    return {"message": "yep bro"}, 200


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


@app.route("/entreprise-slug-site/<slug>", methods=['GET'])
def getsLUGsITE(slug):
    all_users = SiteEntreprise.query.filter_by(name = slug).first()
    result = siteEntreprise.dump(all_users)

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
        activity = request.json['activity']
        user.tel = tel
        user.activity = activity
        db.session.commit()
        return True, 200

    @jwt_required()
    def delete(self,id):
        who = Entreprise.query.get(id)
        
        pos = PositionEntreprise.query.filter_by(entreprise_id = id).all()
        pubs = Pub.query.filter_by(entreprise_id=id).all()
        offers = Offer.query.filter_by(entreprise_id=id).all()
        addPost = AddPost.query.filter_by(entreprise_id=id).all()
        addPro = AddProduct.query.filter_by(entreprise_id=id).all()
        
        site = SiteEntreprise.query.filter_by(
            entreprise_id=id).first()
        if entrepise_schema.dump(Entreprise.query.filter_by(id=id).first())["site"] == True:
             messages = EntrepriseMessage.query.filter_by(
             site_entreprise_id= siteEntreprise.dump(SiteEntreprise.query.filter_by(entreprise_id=id).first())["id"]).all()
             for m in messages:
                db.session.delete(m)
             
            
             for p in pos:
                
                db.session.delete(p)
            
             
             for p2 in pubs:
                 db.session.delete(p2)
             for o in offers:
                 db.session.delete(o)
             for a in addPost:
                 db.session.delete(a)
             for a2 in addPro:
                 db.session.delete(a2)
             db.session.delete(site)

             db.session.delete(who)
        else:

             for p in pos:
                 db.session.delete(p)
             for p2 in pubs:
                 db.session.delete(p2)
             for o in offers:
                 db.session.delete(o)
             for a in addPost:
                 db.session.delete(a)
             for a2 in addPro:
                 db.session.delete(a2)

             db.session.delete(who)
        db.session.commit()
      
api.add_resource(EntrepriseRessource, "/entreprises/<int:id>")


class EntrepriseSiteRessource(Resource):

    def get(self, id):
        user = SiteEntreprise.query.filter_by(entreprise_id = int(id)).first()
        result = siteEntreprise.dump(user)

        return jsonify(result)

    def put(self, id):
        user = SiteEntreprise.query.filter_by(entreprise_id=int(id)).first()
        entreprise = Entreprise.query.filter_by(id=int(id)).first()
        name = request.json['name']
        logo = request.json['logo']
        activity = request.json['activity']
        profil = request.json['profil']
        description = request.json['description']
        outro = request.json['outro']
        tel = request.json['tel']
        web = request.json['web']
        position = request.json['position']
        disposition = request.json['disposition']
        on = request.json['status']["on"]
        off = request.json['status']["off"] 
        pres = request.json['prop']["pres"]
        prod = request.json['prop']["pro"] 
        

        user.tel = tel
        user.activity = activity
        user.name = name.lower().replace(" ", "-")
        user.logo = logo
        user.profil = profil
        user.description_position = description
        user.outro = outro
        user.site = web
        user.on = on
        user.off = off
        user.pres = pres
        user.prod = prod
        user.disposition = disposition

        positionsQuery = PositionEntreprise.query.filter_by(entreprise_id = id).all()

        for p in positionsQuery:
            db.session.delete(p)

        with db.session.no_autoflush:
            for p in position:
                entreprise.position.append(PositionEntreprise(p["value"]))

        db.session.commit()
        return True, 200



api.add_resource(EntrepriseSiteRessource, "/entreprise-site/<int:id>")


@app.route("/entreprise", methods=['POST'])
def postEntreprise():
    username = request.json['username']
    p = request.json['password']
    users = Entreprise.query.filter_by(
        username=username).all()
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
    new_user = Entreprise(username, tel, sec_pas)
    verif_user_exist = Entreprise.query.filter_by(
        tel=tel, username=username.lower().replace(" ", "-")).first()
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
        disposition = request.json['disposition']
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
        school.disposition = disposition
        
        school.description = str(description)
        school.outro = str(outro)
        
        school.tel = tel
        positionsQuery = Position.query.filter_by(school_id = id).all()
        typesQuery = Types.query.filter_by(school_id = id).all()

        for p in positionsQuery:
            db.session.delete(p)
        for t in typesQuery:
            db.session.delete(t)


        
        with db.session.no_autoflush:
            for p in positions:
                school.position.append(Position(p["value"]))

            try:
                for t in types:
                    school.types.append(Types(t["value"]))
            except:
                school.types.append(Types(types["value"]))

                        
        
        
        

        db.session.commit()
       

        return True, 200

    @jwt_required()
    def delete(self, id):
        positionsQuery = Position.query.filter_by(school_id = id).all()
        typesQuery = Types.query.filter_by(school_id = id).all()
        pos = AddPost.query.filter_by(school_id = id).all()
        spe = Speciality.query.filter_by(school_id = id).all()


        messages = SchoolMessage.query.filter_by(
            school_id= id).all()
        
       
        for m in messages:
            db.session.delete(m)

        for s in spe:
            db.session.delete(s)
             

        for p in positionsQuery:
            db.session.delete(p)
        for t in typesQuery:
            db.session.delete(t)
        for p in pos:
            db.session.delete(p)

        school2 = School.query.get(id)
        db.session.delete(school2)
        db.session.commit()

        


api.add_resource(SchoolRessource, "/schools/<int:id>")



@app.route("/addStatSchool/<int:id>", methods=['PUT'])
def addStatSchool(id):
    school = School.query.get(id)
    now = int(school.stat) 
    school.stat = now + 1
    db.session.commit()

    return {"msg": True}, 200


@app.route("/addStatPub/<int:id>", methods=['PUT'])
def addStatPub(id):
    school = Pub.query.get(id)
    now = int(school.stat)
    school.stat = now + 1
    db.session.commit()

    return {"msg": True}, 200

@app.route("/addStatOffer/<int:id>", methods=['PUT'])
def addStatOffer(id):
    school = Offer.query.get(id)
    now = int(school.stat)
    school.stat = now + 1
    db.session.commit()

    return {"msg": True}, 200


@app.route("/addStatEntrepriseSite/<int:id>", methods=['PUT'])
def addStatEntrepriseSite(id):
    school = SiteEntreprise.query.get(id)
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

@app.route("/ToggleStatusPub/<int:id>", methods=['PUT'])
def ToggleStatusPub(id):
    school = Pub.query.get(id)
    school.valid = not school.valid
    school.demande = False
    
    db.session.commit()

    return {"msg": True}, 200

@app.route("/ToggleStatusOffre/<int:id>", methods=['PUT'])
def ToggleStatusOffre(id):
    school = Offer.query.get(id)
    school.valid =  not school.valid
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


@app.route("/ToggleStatusEntreprise/<int:id>", methods=['PUT'])
def ToggleStatusEntreprise(id):
    school = Entreprise.query.get(id)
    school.pro = True
    school.demande = False
    
    db.session.commit()

    return {"msg": True}, 200


@app.route("/TogglevStatusEntreprise/<int:id>", methods=['PUT'])
def ToggleStatusvEntreprise(id):
    school = Entreprise.query.get(id)
    school.pro = not school.pro
    school.demande = False
    db.session.commit()

    return {"msg": True}, 200

@app.route("/DelStatusEntreprise/<int:id>", methods=['PUT'])
def DelToggleStatusEntreprise(id):
    school = Entreprise.query.get(id)
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
    if result == {}:
        return {"msg": "not"}

    if result["id"] is None:
        return False,500

    return jsonify(result)

@app.route("/entreprise/get/<slug>", methods=['GET'])
def get_slug_entreprises(slug):
    all_users = Entreprise.query.filter_by(username = slug.replace(" ","-")).first()
    result = entrepise_schema.dump(all_users)
    if result == {}:
        return {"msg": "nothing"}

    if result["id"] is None:
        return False,500

    return jsonify(result)


@app.route("/entreprises-sites/<int:id>", methods=['GET'])
def get_site_entreprises(id):
    all_users = Entreprise.query.filter_by(
        id=id).first()
    result = entrepise_schema.dump(all_users)
    if result == {}:
        return {"msg": "nothing"}

    if result["id"] is None:
        return False, 500

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
    disposition = request.json['disposition']
    outro = request.json['outro']
    tel = request.json['tel']
    pas = request.json['password']
    pas = bcrypt.generate_password_hash(pas)
    position = request.json['position']
    types = request.json['type']





    new_school = School(name=name, password=pas, tel=tel, description=description, disposition=int(disposition), sigle=sigle,
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


@app.route("/add-site-entreprise", methods=['POST'])
def addSiteEntreprise():

    name = request.json['name']
    logo = request.json['logoName']
    activity = request.json['activity']
    profil = request.json['profilName']
    description = request.json['description']
    disposition = request.json['disposition']
    outro = request.json['outro']
    tel = request.json['tel']
    web = request.json['web']
    position = request.json['position']
    entreprise_id = request.json['entrepriseId']
    on = request.json['status']["on"]
    off = request.json['status']["off"] 
    pres = request.json['prop']["pres"]
    prod = request.json['prop']["pro"] 

    new_school = SiteEntreprise(name=name.lower().replace(" ","-"), site = web,pres=pres,prod=prod,disposition=disposition, offline = off,online = on,activity=activity, tel=tel, description_position=description,
                                logo=logo, profil=profil, outro=outro)

    verif_user_exist = SiteEntreprise.query.filter_by(
        tel=tel, name=name).first()
    if verif_user_exist is None:
        entreprise = Entreprise.query.filter_by(id = int(entreprise_id)).first()
        entreprise.entrepriseSite.append(new_school)
        entreprise.site = True
        with db.session.no_autoflush:
            for posi in position:
                new_position = PositionEntreprise(posi["value"])
                db.session.add(new_position)
                entreprise.position.append(new_position)
            db.session.add(new_school)
        db.session.commit()
        

        return jsonify(siteEntreprise.dump(new_school)), 200
    else:
        abort(409, message="La ressource existe déja")

    




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

@app.route("/get-all-post", methods = ["GET"])
def getEveryPost():
    all_users = AddPost.query.all()
    result = addPostsSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-all-pres", methods = ["GET"])
def getEveryPres():
    all_users = AddProduct.query.all()
    result = addProductsSchema.dump(all_users)

    return jsonify(result), 200



@app.route("/get-entreprises-posts/<int:id>", methods = ["GET"])
def getCustomPosts(id):
    all_users = AddPost.query.filter_by(proprio = True,entreprise_id=id).all()
    result = addPostsSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-entreprises-site-posts/<int:id>", methods = ["GET"])
def getCustomSitePosts(id):
    entreprise = Entreprise.query.get(id)
    all_users = AddPost.query.filter_by(proprio = True,entreprise_id=entreprise.id).all()
    result = addPostsSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-school-posts/<int:id>", methods = ["GET"])
def getCustomSchoolPosts(id):
    all_users = AddPost.query.filter_by(proprio = False,school_id=id).all()
    result = addPostsSchema.dump(all_users)

    return jsonify(result), 200




@app.route("/get-products/<int:id>", methods=["GET"])
def getCustomSiteProducts(id):
    all_users = AddProduct.query.filter_by(
         entreprise_id=id).all()

    result = addProductsSchema.dump(all_users)

    return jsonify(result), 200


@app.route("/get-site-products/<int:id>", methods=["GET"])
def getCustomSite2Products(id):
    all_users = AddProduct.query.filter_by(
         entreprise_id=id).all()

    result = addProductsSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-pubs", methods = ["GET"])
def getAllPubs():
    all_users = Pub.query.all()

    result = pubsSchema.dump(all_users)

    return jsonify(result), 200


@app.route("/get-fines-pubs", methods = ["GET"])
def getFineAllPubs():
    all_users = Pub.query.filter_by(valid=True)

    result = pubsSchema.dump(all_users)
    out = []
    for res in result:
        if(reverse_verif_date(res["available"].split("-")) and verif_date(res['days'].split("-"))):
            out.append(res)

    return jsonify(out), 200

@app.route("/get-fines-offers", methods = ["GET"])
def getFineAllOffers():
    all_users = Offer.query.filter_by(valid=True)

    result = offersSchema.dump(all_users)
    out = []
    for res in result:
        if(verif_date(res['expire'].split("-"))):
            out.append(res)

    return jsonify(out), 200


@app.route("/get-offers", methods = ["GET"])
def getAllOffers():
    all_users = Offer.query.all()

    result = offersSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-site-offers/<int:id>", methods = ["GET"])
def getAllSiteOffers(id):
    all_users = Offer.query.filter_by(entreprise_id=id).all()

    result = offersSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-pubs/<int:id>", methods = ["GET"])
def getCustomPubs(id):
    all_users = Pub.query.filter_by(entreprise_id=id).all()

    result = pubsSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/get-site-pubs/<int:id>", methods = ["GET"])
def getCustomSitePubs(id):
  

    all_users = Pub.query.filter_by(entreprise_id=id).all()

    result = pubsSchema.dump(all_users)

    return jsonify(result), 200


@app.route("/get-offers/<int:id>", methods = ["GET"])
def getCustomOffers(id):
    all_users = Offer.query.filter_by(entreprise_id=id).all()

    result = offersSchema.dump(all_users)

    return jsonify(result), 200

@app.route("/entreprises-sites", methods = ["GET"])
def getAllEntrepriseSite():
    all_users = SiteEntreprise.query.all()

    result = sitesEntreprise.dump(all_users)

    return jsonify(result), 200


@app.route("/add-post-entreprise/<int:id>", methods=['POST'])
def addPostEntreprise(id):
    image = request.json['media']
    name = request.json['name']
    outro = request.json['outro']
    disposition = request.json['disposition']

    post_exist = AddPost.query.filter_by(name=name,image=image).first()

    if post_exist is None:
        
        new_post = AddPost(image=image,description=outro,disposition=disposition,name=name,proprio = True)    
        entreprise = Entreprise.query.filter_by(
        id=id).first()
        entreprise.addPost.append(new_post)       
        db.session.add(new_post)
        db.session.commit()
        return  jsonify(addPostSchema.dump(new_post)), 200
    else:
        abort(409, message="La ressource existe déja")



@app.route("/add-post-school/<int:id>", methods=['POST'])
def addPostSchool(id):
    image = request.json['media']
    name = request.json['name']
    outro = request.json['outro']
    disposition = request.json['disposition']

    post_exist = AddPost.query.filter_by(name=name,description=outro,image=image).first()

    if post_exist is None:
        
        new_post = AddPost(image=image,description=outro,disposition=disposition,name=name,proprio = False)    
        entreprise = School.query.filter_by(
        id=id).first()
        entreprise.addPost.append(new_post)       
        db.session.add(new_post)
        db.session.commit()
        return  jsonify(addPostSchema.dump(new_post)), 200
    else:
        abort(409, message="La ressource existe déja")



@app.route("/add-product-entreprise/<int:id>", methods=['POST'])
def addProductEntreprise(id):
    image = request.json['media']
    price = request.json['price']
    name = request.json['name']
    proprio = request.json['proprio']

    post_exist = AddPost.query.filter_by(image=image).first()

    if post_exist is None:

        if(proprio == "entreprise"):
            new_post = AddProduct(image=image, price=price,name=name,
                                proprio=True)
            entreprise = Entreprise.query.filter_by(
                id=id).first()
            entreprise.addProduct.append(new_post)

        db.session.add(new_post)
        db.session.commit()
        return jsonify(addProductSchema.dump(new_post)), 200
    else:
        abort(409, message="La ressource existe déja")


@app.route("/add-pub-entreprise/<int:id>", methods=['POST'])
def addPubEntreprise(id):
    
    logo = request.json['logo']
    days = request.json['days']
    date = request.json['date']
    name = request.json['name']
    post_exist = Pub.query.filter_by(available=date,name=logo,days=days,entreprise_id=id).first()

    if post_exist is None:
        new_post = Pub(name=name, media=logo,days=days,available=date,
                            proprio=True)
        entreprise = Entreprise.query.filter_by(
            id=id).first()
        entreprise.pub.append(new_post)

        db.session.add(new_post)
        db.session.commit()

        return jsonify(pubSchema.dump(new_post)), 200
    else:
        return {"id": False}, 500
 

@app.route("/add-offer-entreprise/<int:id>", methods=['POST'])
def addOfferEntreprise(id):
    outro = request.json['outro']
    logo = request.json['logo']
    objet = request.json['objet']
    tel = request.json['tel']
    url = request.json['url']
    expiration = request.json['expiration']

    post_exist = Offer.query.filter_by(title=objet,entreprise_id=id).first()

    if post_exist is None:
        new_post = Offer(title=objet, tel=tel, logo=logo, content=outro, url=url, expire = expiration,
                    proprio=True)
        entreprise = Entreprise.query.filter_by(
            id=id).first()
        entreprise.offer.append(new_post)

        db.session.add(new_post)
        db.session.commit()
        return jsonify(offerSchema.dump(new_post)), 200
    else:
        return {"result": False}, 500


class AddProductRessource(Resource):

  @jwt_required()
  def put(self, id):
      user = AddProduct.query.get(id)
      image = request.json['image']
      name = request.json['name']
      price = request.json['price']
      user.name = name
      user.image = image
      user.price = price

      db.session.commit()
      return True, 200

  @jwt_required()
  def delete(self, id):
      filiaire = AddProduct.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()


api.add_resource(AddProductRessource, "/products/<int:id>")






class OffersRessource(Resource):

  
  @jwt_required()
  def put(self, id):
      user = Offer.query.get(id)
      outro = request.json['outro']
      logo = request.json['logo']
      objet = request.json['objet']
      tel = request.json['tel']
      url = request.json['url']
      expiration = request.json['expiration']
      user.content = outro
      user.logo = logo
      user.title = objet
      user.tel = tel
      user.url = url
      user.expire = expiration

      db.session.commit()
      return True, 200





  @jwt_required()
  def delete(self, id):
      filiaire = Offer.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()


api.add_resource(OffersRessource, "/offers/<int:id>")


class PubRessource(Resource):

  @jwt_required()
  def put(self, id):
      user = Pub.query.get(id)
      logo = request.json['logo']
      days = request.json['days']
      date = request.json['date']
      name = request.json['name']
      user.name = name
      user.media = logo
      user.days = days
      user.available = date

      db.session.commit()
      return True, 200

  @jwt_required()
  def delete(self, id):
      filiaire = Pub.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()


api.add_resource(PubRessource, "/pubs/<int:id>")







class AddPostRessource(Resource):

  
  @jwt_required()
  def put(self, id):
      user = AddPost.query.get(id)
      image = request.json['media']
      name = request.json['name']
      outro = request.json['outro']
      disposition = request.json['disposition']
      user.name = name
      user.image = image
      user.description = outro
      user.disposition = disposition

      db.session.commit()
      return True, 200





  @jwt_required()
  def delete(self, id):
      filiaire = AddPost.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()


api.add_resource(AddPostRessource, "/posts/<int:id>")









@app.route("/demande/<int:id>", methods = ["PUT"])
def getCustomDemande(id):
    school = School.query.filter_by(id = id).first()
    school.demande = not school.demande
    if school.demande: school.create_at = datetime.utcnow()
    db.session.commit()

    return {}, 200

@jwt_required()
@app.route("/demande-entreprise/<int:id>", methods = ["PUT"])
def getCustomDemandeEntreprise(id):
    school = Entreprise.query.filter_by(id = id).first()
    school.demande = not school.demande
    site  = SiteEntreprise.query.filter_by(entreprise_id = id).first()
    if school.demande: site.create_at = datetime.utcnow()
    db.session.commit()

    return {}, 200



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
        
        tab.append({"user": user_schema.dump(User.query.get(
            r["user_id"])), "message": school_message_schema.dump(SchoolMessage.query.get(r["id"]))})
        

  
    return jsonify(tab), 200
    

    


class MessageRessource(Resource):


  @jwt_required()
  def delete(self, id):
      filiaire = SchoolMessage.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()

     
api.add_resource(MessageRessource, "/messages/<int:id>")


@app.route("/message-entreprise", methods=['POST'])
def addEMesasage():
    userId = int(request.json['userId'])
    schoolId = int(request.json['schoolId'])
    message = request.json['message']

    school = SiteEntreprise.query.filter_by(entreprise_id=schoolId).first()
    user = User.query.filter_by(id=userId).first()

    mes = EntrepriseMessage(message=message)

    with db.session.no_autoflush:
        school.message.append(mes)
        user.entrepriseMessage.append(mes)
    db.session.add(mes)
    db.session.commit()
    return {"ms": True},200
 

@app.route("/messages-entreprise/<int:id>", methods=['GET'])
def getEMesasage(id):
    
    school = SiteEntreprise.query.filter_by(entreprise_id=id).first()


    mes = EntrepriseMessage.query.order_by(EntrepriseMessage.id.desc()).filter_by(site_entreprise_id= school.id).all()
    result = entreprises_message_schema.dump(mes)
    tab = []
    for r in result:
        
        tab.append({"user": user_schema.dump(User.query.get(
            r["user_id"])), "message": entreprise_message_schema.dump(EntrepriseMessage.query.get(r["id"]))})
        

  
    return jsonify(tab), 200
    

    


class MessageERessource(Resource):


  @jwt_required()
  def delete(self, id):
      filiaire = EntrepriseMessage.query.get(id)
      db.session.delete(filiaire)
      db.session.commit()

     
api.add_resource(MessageERessource, "/messages-entreprise/<int:id>")

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


@app.route("/entreprises-positions/<int:id>", methods=["GET"])
def getEntreprisePositions(id):
    all_users = PositionEntreprise.query.filter_by(entreprise_id = id).all()
    result = positions_entreprise_schema.dump(all_users)
    print(result)

    return jsonify(result),200


@app.route("/entreprises-site-positions/<int:id>", methods=["GET"])
def getSiteEntreprisePositions(id):
    entreprise = Entreprise.query.get(id)
    all_users = PositionEntreprise.query.filter_by(entreprise_id=entreprise.id).all()
    result = positions_entreprise_schema.dump(all_users)
    print(result)

    return jsonify(result), 200

@app.route("/custom-positions/<int:id>", methods=["GET"])
def getCustomPositions(id):
    all_users = Position.query.filter_by(school_id = id).all()
    result = positions_schema.dump(all_users)

    return jsonify(result),200

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
    description = request.json['description']
    prix = request.json['price']
    who = request.json['who']
    school_id = int(school_id)
    school = School.query.filter_by(id=school_id).first()
    spe_exist = Speciality.query.filter_by(
        name=name, school_id=school_id).first()


    if spe_exist is None:     
        new_spe = Speciality(name, prix, description, who)
        with db.session.no_autoflush:
            school.speciality.append(new_spe)
        db.session.add(new_spe)
        db.session.commit()
        
        return jsonify(speciality_schema.dump(new_spe)), 200
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
      price = request.json['price']
      description = request.json['description']
      who = request.json['who']
      user.name = name
      user.price = price
      user.description = description
      user.who = who
      

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
    app.run(debug=True,host="0.0.0.0")
