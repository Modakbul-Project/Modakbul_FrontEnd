import oauth2client.client
from flask import Flask, render_template, request, redirect, session, url_for, json
from authlib.integrations.flask_client import OAuth
from apiclient import discovery
import os

app = Flask(__name__) #플라스크 애플리케이션 생성, name=모듈명=pybo.py

app.config['SECRET_KEY']=os.urandom(12)
oauth = OAuth(app)
with open('./static/client_secret2.json') as f:
    json_data=json.load(f)

@app.route('/testcal')
def testcal():
    calendars = []
    service = discovery.build('calendar', 'v3', oauth.google.authorize_access_token)
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

@app.route('/makepage')
def make_page():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('makemeet.html')
    else:
        return redirect('/login')

@app.route('/mymeets')
def my_meets():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('mypage.html', mypage=1)
    else:
        return redirect('/login')

@app.route('/pfedit')
def profile_edit():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('profileedit.html')
    else:
        return redirect('/login')

@app.route('/meet')
def meet():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('meetpage.html', admin=0)
    else:
        return redirect('/login')


@app.route('/makenotice')
def make_notice():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('makenotice.html')
    else:
        return redirect('/login')

@app.route('/meetadmin')
def meet_admin():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('meetpage.html', admin=1)
    else:
        return redirect('/login')


@app.route('/profile')
def profile():
    if 'user' in session:  # 로그인 여부 확인
        return render_template('profile.html')
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
    app.run('0.0.0.0', port=5000, debug=True)
