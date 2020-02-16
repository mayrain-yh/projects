#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Video,Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'videos':Video.query.order_by('create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/ashore/',methods=['GET','POST'])
def ashore():
    if request.method == 'GET':
        return render_template('ashore.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permant = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码错误'



@app.route('/install/',methods=['GET','POST'])
def install():
    if request.method == 'GET':
        return render_template('install.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，不可重复
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            #password1要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核对再填写！'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，就让页面跳转
                return redirect(url_for('ashore'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('ashore'))

@app.route('/release/',methods=['GET','POST'])
@login_required
def release():
    if request.method == 'GET':
        return render_template('release.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        video = Video(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        video.author = user
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<video_id>/')
def detail(video_id):
    video_model = Video.query.filter(Video.id == video_id).first()
    return render_template('detail.html',video=video_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    vedio_id = request.form.get('vedio_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user.id).first()
    answer.author = user
    vedio = Vedio.query.fileter(Vedio.id == vedio_id).first()
    answer.vedio = vedio
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',vedio_id =vedio_id ))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()

