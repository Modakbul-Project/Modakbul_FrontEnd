from flask import Flask, render_template, request, redirect, session, url_for, json
from authlib.integrations.flask_client import OAuth
#from apiclient import discovery #캘린더 제작용
import os

from bson.objectid import ObjectId
from pymongo import MongoClient

from flask_socketio import SocketIO, join_room
app = Flask(__name__) #플라스크 애플리케이션 생성
app.config['SECRET_KEY']=os.urandom(12)
oauth = OAuth(app)
socketio = SocketIO(app)
with open('./static/client_secret2.json') as f:
    json_data=json.load(f)

##
@app.route('/mongo',methods=['GET'])
def mongoTest():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.modakbul
    collection = db.test
    results = collection.find()
    #client.close()
    return render_template('mongo.html', data=results)

@app.route('/')
def test():
    if 'user' in session:
        print(session['user'])
    else:
        print('no login')

    return render_template('main.html')

@app.route('/mypage')
def my_page():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('mypage.html', mypage=0)
    else:
        return redirect('/login')

@app.route('/mymeets')
def my_meets():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('mypage.html', mypage=1)
    else:
        return redirect('/login')

@app.route('/meet/<id>')
def meet_page(id=None):
    if 'user' in session:  # 로그인 여부 확인
        #db 불러오기
        client = MongoClient('mongodb://localhost:27017/')
        db = client.modakbul
        collection = db.modakbul

        #모임id로 채팅방이름 만들기
        session['room'] = id

        #테이블에 모임id필드 추가하여 id에 맞는 로그만 불러오기
        chatLog = db.chatLog.find({'room': id})
        results = collection.find({'room': id})
        return render_template('meetpage.html', admin=0, data=results, user=session['user']['name'], chatLog = chatLog)
    else:
        return redirect('/login')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.modakbul
    collection = db.chatLog

    print('received my event: ' + str(json))
    json['user'] = session['user']['name']
    json['userimg'] = session['user']['picture']
    if 'data' in json:
        join_room(session.get('room'))
    else:
        result = collection.insert_one(
            {"message": json["message"], "user": json["user"], "userimg": json["userimg"], "room": session.get('room')})

    socketio.emit('my response', json, room=session.get('room'))

@socketio.on('postit')
def postit(json,methods=['GET', 'POST']):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.modakbul
    collection = db.modakbul
    if 'data' in json:
        print('connect postit')
        join_room(session.get('room'))
    else:
        json['user'] = session['user']['name']
        if json['id'] == 'None':
            result = collection.insert_one(
                {"x": json["x"], "y": json["y"], "message": json["message"], "user": session["user"]["name"], "room": session.get('room')})
            json['id'] = str(result.inserted_id)
            socketio.emit('newpostit', json, room=session.get('room'))
        elif 'del' in json:
            if json['user'] == session['user']['name']:
                collection.delete_one({"_id": ObjectId(json["id"])})
                socketio.emit('delres',json, room=session.get('room'))
        else:
            result = collection.update_one({"_id": ObjectId(json["id"])},
                                           {"$set": {"x": json["x"], "y": json["y"], "message": json["message"]}})
            socketio.emit('postitres', json, room=session.get('room'))



@app.route('/meetadmin')
def meet_admin():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('meetpage.html', admin=1)
    else:
        return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/google/')
def google():
    GOOGLE_CLIENT_ID = json_data['web']['client_id']
    GOOGLE_CLIENT_SECRET = json_data['web']['client_secret']
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = token.get('userinfo')
    tok = token.get('access_token')
    if user:
        session['user'] = user
        session['tk'] = tok
    print(" Google User ", user)
    print(" eccess token :  ", tok)
    return redirect('/')

@app.route("/logout", methods=["GET"])
def logout():
  session.clear()
  return redirect('/')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
   # app.run('0.0.0.0', port=5000, debug=True)
