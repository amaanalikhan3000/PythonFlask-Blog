from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, session
# from flask_session import Session
import json
import os
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug import secure_filename
import math
with open('config.json','r') as c:
    params = json.load(c)["params"]


local_server = True

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config['UPLOAD_FOLDER'] = params['upload_location']

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingthunder'
db = SQLAlchemy(app)


class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)



class Posts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    date = db.Column(db.String(12), nullable=True)

    img_file  = db.Column(db.String(12), nullable=True)
    tagline = db.Column(db.String(120), nullable=False)




@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    # page = int(page)
    # posts = int(posts[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])])
    posts = posts[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]

    if(page==1):
        prev = "#"
        next = "/?page="+ str(page+1)

    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"

    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts,prev=prev,next=next)




@app.route("/about")
def about():
    return render_template('about.html',params=params)





@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard():


    if ('user' in session and session['user']==params['admin_usr']):
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params,posts=posts)

    if request.method =="POST":
        # pass
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if(username ==params['admin_usr'] and  userpass ==params['admin_password']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params,posts=posts)

    return render_template('login.html', params=params)






@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):

    post = Posts.query.filter_by(slug=post_slug).first()

    return render_template('post.html',params=params,post=post)




@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_usr']):
        if (request.method =='POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "uploaded Successfully"

# secure_filename for security


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

# @app.route("/")
# def home():
#     # prev =
#     next = page + 1
#     middle = page - 1






@app.route("/delete/<string:sno>", methods = ['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user'] == params['admin_usr']):

        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)



@app.route("/edit/<string:sno>", methods = ['GET', 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == params['admin_usr']):

#         IF USER IS LOGGED
        if request.method == "POST":
            box_title = request.form.get('title')
            title = request.form.get('tline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            data = datetime.now()


            if sno =='0':
                post = Posts(title=box_title, slug = slug,content=content,img_file=img_file,tagline=tline,date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = slug
                post.tagline = tline
                post.img_file = img_file
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)




        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params,post=post)





app.run(debug=True)




# VIDEO 19 se dekhna hai 3:43 se



