
from pydoc import doc
from sre_constants import SUCCESS
from flask import Flask, jsonify,request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime
import requests
from itsdangerous import json
from bson.json_util import dumps
from bson.objectid import ObjectId

import pymongo
import bcrypt

app = Flask(__name__)
CORS(app)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

# Change this in your code!
app.config["JWT_SECRET_KEY"] = "super-secret"

jwt = JWTManager(app)
db = pymongo.MongoClient('mongodb+srv://parnnaja005:0864680770za@cluster0.chz67.mongodb.net/myFirstDatabase?retryWrites=true&w=majority').datebasegameguide

@app.route("/")
def hello():
   # cluster.username.insert_one({"test1":'test2'})
    return "Hello, World1!"
@app.route('/signup', methods = ['GET', 'POST'])
def singup():
  if request.method =='POST':
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password'].encode('utf-8')
    checkemail = db.user.find({'email': email})
    print(name,email,password)
    try:
      yy = checkemail[0]
      print("มี")
      return "this email has already been used"
    except:
      print("ไม่มี")
      salt = bcrypt.gensalt()
      hashed = bcrypt.hashpw(password,salt)
      p = hashed.decode()
      db.user.insert_one({'name':name,'email':email,'password':p,'credit':0,'blog':[]})
      return "success"
@app.route('/signin', methods = ['GET', 'POST'])
def singin():
  if request.method =='POST':
    data = request.get_json()
    email = data['email']
    password = data['password'].encode('utf-8')
    user = db.user.find({'email':email})
    try :
      yy = user[0]['email']
      try:
        passdb = user[0]['password'].encode('utf-8')
        if bcrypt.checkpw(password,passdb):
          print("match")
          ids = str(user[0]['_id'])
          name = str(user[0]['name'])
          email = str(user[0]['email'])
          credit= str(user[0]['credit'])
          # key = jwk.JWK.generate(kty='RSA', size=2048)
          # key = ''
          # payload = { 'id': ids, 'name': name,"email":email }
          # token = jwt.generate_jwt(payload, key, 'HS256')
          # token = jwt.encode({'id': ids, 'name': name,'email': email},key="",algorithm="HS256")
          # return "Match"
          # return {'status':'singin success',"id":ids,"name":name,"email":email}
          token = create_access_token({ 'id': ids, 'name': name,"email":email,'credit':credit })
          return {'status':'singin success','token':token}
        else:
          print("does not match")
          return {'status':'password is incorrectsssss'}
      except:
        return {'status':'password is incorrect'}
            
    except:
      return {'status':'invalid email'}
@app.route('/postcontent', methods = ['GET', 'POST'])
def postcontent():
   if request.method =='POST':
    data = request.get_json()
    print('kkkkkk',data)
    title = data['title']
    create_by = data['create_by']
    category = data['category']
    credit = data['credit']
    image_id = data['image_id']
    id = data['id']
    content = data['content']
    x = datetime.datetime.now()
    date = x.strftime("%d")+" "+x.strftime("%B")+" "+x.strftime("%Y")
    db.post.insert_one({"iduser":id,"content":content,'title':title,'category':category,'create_by':create_by,'credit':credit,'image_id':image_id,'date':date})
    db.user.update_one({"_id": ObjectId(id)}, {'$inc': {'credit': 15}})
    return {"status":"post success"}

@app.route("/blogs")
def blogs():
    docs = db.post.find()
    data = []
    for i in docs:
        data.append(i)
        print(i)
    return dumps(data)

@app.route("/blogs/<id>")
def blogsdetail(id):
    print(id)
    docs = db.post.find({"_id": ObjectId(id)})
    print(docs)
    data = []
    for i in docs:
        data.append(i)
        print(i)
    return dumps(data)
@app.route('/comment', methods = ['GET', 'POST'])
def comment():
   if request.method =='POST':
    data = request.get_json()
    print('kkkkkk',data)
    userid = data['userid']
    postid = data['postid']
    username = data['username']
    comment = data['comment']
    x = datetime.datetime.now()
    date = x.strftime("%d")+" "+x.strftime("%B")+" "+x.strftime("%Y")
    tt = db.comments.insert_one({"userid":userid,"postid":postid,'username':username,'comment':comment,'date':date,'reply':[]})
    print(tt.inserted_id)
    id = str(tt.inserted_id)
    return {"id":id}
@app.route("/comment/<id>")
def getcomment(id):
    print(id)
    docs = db.comments.find({"postid":id})
    print(docs)
    data = []
    for i in docs:
        data.append(i)
        print(i)
    return dumps(data)
@app.route('/reply', methods = ['GET', 'POST'])
def reply():
   if request.method =='POST':
    data = request.get_json()
    print('kkkkkk',data)
    id_coment = data['id_coment']
    username = data['username']
    comment = data['comment']
    db.comments.update_one({"_id": ObjectId(id_coment)}, {'$push': {'reply': {"comment":comment,"username":username}}})
    return {"status":"post success"}

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      print(f)
      # filename = secure_filename(f.filename)
      # f.save(os.path.join("files/",filename))
      headers = {"Authorization": "Bearer ya29.a0AX9GBdWV_W83JuZ9X4VPGw1Kc2DiLzgu7d-rhJnBj1HePrCVygAs3e3az57rp8-9rV8MwQZrD_du96tCYGhn1Z3j26MnRKKrEl930J5rWFu_d--hE-k-pHcsNcNp7Z7s9KmUiFHkNauZXfs99VvSK3TBTX8KaCgYKATkSARMSFQHUCsbCcq5timFIxBEvX9aKD2AP9A0163"}
      para = {"name": f.filename,
              "parents": ["1SwUwF6v5mzBvR50xX4QEP0krrme0ssem"]
            }
      files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
               'file': f
            }
      r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",headers=headers,files=files)
      image_id = r.json()['id']
      print(image_id)
    #   f.save(secure_filename("files/"+f.filename))
      return {"image_id":image_id}
@app.route("/credit/<id>")
def getcredit(id):
    docs = db.user.find_one({"_id": ObjectId(id)})
    return {'credit':docs['credit']}
@app.route("/deletecredit/<id>/<credit>/<blogid>")
def deletecredit(id,credit,blogid):
    db.user.update_many({"_id": ObjectId(id)}, {'$inc': {'credit': -int(credit)}})
    db.user.update_many({"_id": ObjectId(id)},{'$push': {'blog': blogid}})
    return 'kkkk'
@app.route("/checkblog/<id>/<blogid>")
def checkblog(id,blogid):
    docs = db.user.find_one({"_id": ObjectId(id)},{ 'blog': 1}) 
    if blogid in docs['blog']:
      return "yes"
    else:
      return "no"