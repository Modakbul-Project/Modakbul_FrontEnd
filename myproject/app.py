import json

from flask import Flask, render_template, request, redirect, session, url_for, json
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__) #플라스크 애플리케이션 생성, name=모듈명=pybo.py

app.config['SECRET_KEY']=os.urandom(12)
#app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = './static/client_secret_.json'
oauth = OAuth(app)
with open('./static/client_secret.json') as f:
    json_data=json.load(f)

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
        return render_template('mypage.html')
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
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = token.get('userinfo')
    if user:
        session['user'] = user
    print(" Google User ", user)
    return redirect('/')

@app.route("/logout", methods=["GET"])
def logout():
  session.clear()
  return redirect('/')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
