from multiprocessing import context
from re import T, sub
from flask import Flask,render_template,redirect,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage


#giving access to read data through config.json
with open('config.json', 'r') as j:
    params = json.load(j) ["params"]

#setting local_server to True while development
local_server = True

#initialising flask app
app = Flask(__name__)

#required for emailing through flask
app.secret_key = 'super-secret-key'

#required for uploading a file
app.config['UPLOAD_FOLDER'] = params['upload_location']

#setting up SMTP server email feetching
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'])

#initialising flask_mail
mail = Mail(app)


#configuring database to flask
if local_server == params['local_server']:
    app.config['SQLALCHEMY_DATABASE_URI'] =  params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


#initializing mysql 
db = SQLAlchemy(app)


'''contact section!'''
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(520), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/contact")
def contact():
    return render_template('contact.html', params = params)


@app.route("/", methods = ['GET', 'POST'])
def home():
    if(request.method=='POST'):
        flash("Your request has been sent.I'll get back to you soon!","success")
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        dbentry = Contacts(name=name, email = email, phone_num = phone, msg = message, date= datetime.now() )
        db.session.add(dbentry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                        sender = email,
                        recipients = [params['gmail-user']],
                        body = message + "\n" + phone)    
    return render_template('index.html', params = params)



'''mail_listing section!'''
class Mail_listing(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(15), nullable=True)


@app.route("/mail_listing", methods = ['GET', 'POST'])
def mail_listing():
    if(request.method=='POST'):
        '''Add entry to the database'''
        mname = request.form.get('name')
        memail = request.form.get('email')          
        mail_entry = Mail_listing(name=mname, email = memail, date= datetime.now() )
        db.session.add(mail_entry)
        db.session.commit()    
    return render_template('mail_listing.html', params = params)
    


'''Posts section!'''
class Python_posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=True)
    slug = db.Column(db.String(35), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.String(10), nullable=True)
  # img_file = db.Column(db.String(12), nullable=True)


@app.route("/python/python_post/<string:python_post_slug>", methods=['GET'])
def python_posts(python_post_slug):
    python_post = Python_posts.query.filter_by(slug=python_post_slug).first()
    python_posts = Python_posts.query.filter_by().all()
    return render_template("python_post.html", python_post=python_post, python_posts=python_posts, params=params)


@app.route('/python')
def python():
    python_posts = Python_posts.query.filter_by().all()
    return render_template("python.html", params=params, python_posts=python_posts)



class Database_posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=True)
    slug = db.Column(db.String(35), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.String(10), nullable=True)
  # img_file = db.Column(db.String(12), nullable=True)


@app.route("/database/database_post/<string:database_post_slug>", methods=['GET'])
def database_posts(database_post_slug):
    database_post = Database_posts.query.filter_by(slug=database_post_slug).first()
    database_posts = Database_posts.query.filter_by().all()
    return render_template("database_post.html", database_post=database_post, database_posts=database_posts, params=params)


@app.route('/database')
def database():
    database_posts = Database_posts.query.filter_by().all()
    return render_template("database.html", params=params, database_posts=database_posts)



class Automation_posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(50), nullable=True)
    slug = db.Column(db.String(35), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.String(10), nullable=True)
  # img_file = db.Column(db.String(12), nullable=True)


@app.route("/automation/automation_post/<string:automation_post_slug>", methods=['GET'])
def automation_posts(automation_post_slug):
    automation_post = Automation_posts.query.filter_by(slug=automation_post_slug).first()
    automation_posts = Automation_posts.query.filter_by().all()
    return render_template("automation_post.html", automation_post=automation_post, automation_posts=automation_posts, params=params)


@app.route('/automation')
def automation():
    automation_posts = Automation_posts.query.filter_by().all()
    return render_template("automation.html", params=params, automation_posts=automation_posts)



''' Admin panel section! '''
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard.html', params = params)
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == params['admin_user'] and userpass == params['admin_password']:
            #set session variable
            session['user'] = username
            return render_template('dashboard.html', params=params)
    return render_template("index.html", params=params)


@app.route("/uploader" , methods=['GET', 'POST'])
def uploader():
    if "user" in session and session['user']==params['admin_user']:
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully!"


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")



@app.route("/python_dash", methods=['GET', 'POST'])
def python_dash():
    if ('user' in session and session['user'] == params['admin_user']):
        python_posts = Python_posts.query.all()  # to manage posts if user already in admin panel
        return render_template('python_dash.html', params = params, python_posts = python_posts)
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == params['admin_user'] and userpass == params['admin_password']:
            #set session variable
            session['user'] = username
            # to manage posts in admin panel
            python_posts = Python_posts.query.all() 
            return render_template('python_dash.html', params=params, python_posts = python_posts)
    return render_template("index.html", params=params)


@app.route('/python_edit/<string:sno>', methods = ['GET', 'POST'])
def python_edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get("title")
            sub =  request.form.get("subtitle")  # html and python variables can be different!!!
            slug =  request.form.get("slug")
            content =  request.form.get("content")
           # img_file =  request.form.get("img_file")
            date = datetime.now()
            if sno == "0": # 0 is a text here!
                python_post = Python_posts(title = box_title, subtitle = sub, slug = slug, content = content,  date = date)
                db.session.add(python_post)
                db.session.commit()
            else:
                python_post = Python_posts.query.filter_by(sno = sno).first()
                python_post.title = box_title
                python_post.subtitle = sub
                python_post.slug = slug
                python_post.content = content
                #python_post.img_file = img_file
                python_post.date = date
                db.session.commit()
                return redirect('/python_edit/'+sno)
        python_post = Python_posts.query.filter_by(sno=sno).first()
        return render_template('python_edit.html',params = params, python_post = python_post,sno=sno)


@app.route("/python_delete/<string:sno>" , methods=['GET', 'POST'])
def delete_python_post(sno):
    if "user" in session and session['user']==params['admin_user']:
        python_post = Python_posts.query.filter_by(sno=sno).first()
        db.session.delete(python_post)
        db.session.commit()
    return redirect("/python_dash")



@app.route("/database_dash", methods=['GET', 'POST'])
def database_dash():
    if ('user' in session and session['user'] == params['admin_user']):
        database_posts = Database_posts.query.all()  # to manage posts if user already in admin panel
        return render_template('database_dash.html', params = params, database_posts = database_posts)
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == params['admin_user'] and userpass == params['admin_password']:
            #set session variable
            session['user'] = username
            # to manage posts in admin panel
            database_posts = Database_posts.query.all() 
            return render_template('database_dash.html', params=params, database_posts = database_posts)
    return render_template("index.html", params=params)


@app.route('/database_edit/<string:sno>', methods = ['GET', 'POST'])
def database_edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get("title")
            sub =  request.form.get("subtitle")  # html and python variables can be different!!!
            slug =  request.form.get("slug")
            content =  request.form.get("content")
           # img_file =  request.form.get("img_file")
            date = datetime.now()
            if sno == "0": # 0 is a text here!
                database_post = Database_posts(title = box_title, subtitle = sub, slug = slug, content = content,  date = date)
                db.session.add(database_post)
                db.session.commit()
            else:
                database_post = Database_posts.query.filter_by(sno = sno).first()
                database_post.title = box_title
                database_post.subtitle = sub
                database_post.slug = slug
                database_post.content = content
                #python_post.img_file = img_file
                database_post.date = date
                db.session.commit()
                return redirect('/database_edit/'+sno)
        database_post = Database_posts.query.filter_by(sno=sno).first()
        return render_template('database_edit.html',params = params, database_post = database_post,sno=sno)


@app.route("/database_delete/<string:sno>" , methods=['GET', 'POST'])
def delete_database_post(sno):
    if "user" in session and session['user']==params['admin_user']:
        database_post = Database_posts.query.filter_by(sno=sno).first()
        db.session.delete(database_post)
        db.session.commit()
    return redirect("/database_dash")



@app.route("/automation_dash", methods=['GET', 'POST'])
def automation_dash():
    if ('user' in session and session['user'] == params['admin_user']):
        automation_posts = Automation_posts.query.all()  # to manage posts if user already in admin panel
        return render_template('automation_dash.html', params = params, automation_posts = automation_posts)
    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == params['admin_user'] and userpass == params['admin_password']:
            #set session variable
            session['user'] = username
            # to manage posts in admin panel
            automation_posts = Automation_posts.query.all() 
            return render_template('automation_dash.html', params=params, automation_posts = automation_posts)
    return render_template("index.html", params=params)


@app.route('/automation_edit/<string:sno>', methods = ['GET', 'POST'])
def automation_edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get("title")
            sub =  request.form.get("subtitle")  # html and python variables can be different!!!
            slug =  request.form.get("slug")
            content =  request.form.get("content")
           # img_file =  request.form.get("img_file")
            date = datetime.now()
            if sno == "0": # 0 is a text here!
                automation_post = Automation_posts(title = box_title, subtitle = sub, slug = slug, content = content,  date = date)
                db.session.add(automation_post)
                db.session.commit()
            else:
                automation_post = Automation_posts.query.filter_by(sno = sno).first()
                automation_post.title = box_title
                automation_post.subtitle = sub
                automation_post.slug = slug
                automation_post.content = content
                #python_post.img_file = img_file
                automation_post.date = date
                db.session.commit()
                return redirect('/automation_edit/'+sno)
        automation_post = Automation_posts.query.filter_by(sno=sno).first()
        return render_template('automation_edit.html',params = params, automation_post = automation_post,sno=sno)



@app.route("/automation_delete/<string:sno>" , methods=['GET', 'POST'])
def delete_automation_post(sno):
    if "user" in session and session['user']==params['admin_user']:
        automation_post = Automation_posts.query.filter_by(sno=sno).first()
        db.session.delete(automation_post)
        db.session.commit()
    return redirect("/automation_dash")



if __name__=='__main__':
    app.run(debug=True)