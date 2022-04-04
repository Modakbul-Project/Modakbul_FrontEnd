from flask import Flask, render_template, request, redirect, session, url_for
from oauth2client.contrib.flask_util import UserOAuth2

app = Flask(__name__) #플라스크 애플리케이션 생성, name=모듈명=pybo.py

app.config['SECRET_KEY']='test'
app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = './static/client_secret_.json'
oauth2 = UserOAuth2(app)
@app.route('/')
def test():
    if oauth2.has_credentials():#로그인 여부 확인
        print('login OK')
    else:
        print('login NO')
    return render_template('main.html')

@app.route('/mypage')
@oauth2.required
def my_page():
    return render_template('mypage.html')

@app.route("/logout", methods=["GET"])
def logout():
  session.clear()
  return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
