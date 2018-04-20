from flask import Flask, request, redirect, render_template, flash, session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "weioha8e8aehfaservhnskeh"


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='user_id')

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User(username='%s') ID(id='%s')>" % (self.username, self.id)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self,title,body,user_id):
        self.title = title
        self.body = body
        self.user_id=user_id

    def __repr__(self):
        return "<Blog(title='%s', body='%s')>" % (self.title, self.body)


@app.route("/logoff")
def logout():
    #delete user from session
    del session["username"]
    return redirect("/")


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #validate stuff and return flash messages

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            # TODO - user better response messaging with flash
            return "<h1>Username already taken!</h1>"
    
    return render_template("signup.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #check username

        #check password

        #if username and password correct
        session["username"] = username
        print(session)
        return redirect("/newpost")
        ##elif username not in system
        #return redirect("signup.html")

    return render_template("login.html")

#@app.route("/index")
#def index():

@app.route("/blog")
def blog():
    blogs = Blog.query.all()
    users = User.query.all()

    if request.method == "GET" and request.args.get("postid"):
        blog_id = request.args.get("id")
        blogs = Blog.query.get(blog_id)
        if blogs:
            return render_template("blog.html",title="New Post",blogs=[blogs])

    if request.method == "GET" and request.args.get("userid"):
        userid = request.args.get("userid")
        user = User.query.get(userid)
        user_id = user.id
        blogs = Blog.query.get(user_id)
        return render_template("blog.html",title=user.username +  " Posts",blogs=[blogs])

    return render_template("blog.html",blogs=blogs,users=users)

@app.route("/newpost",methods = ["POST","GET"])
def new_post():
    if request.method == "POST":
        blog_title = request.form["title"]
        blog_body = request.form["body"]
        if blog_title:
            blog_title.strip()
        if blog_body:
            blog_body.strip()

        if not blog_title and not blog_body:
            msg_title = "There is no title"
            flash(msg_title,'title')
            msg_body = "There is no body"
            flash(msg_body,'body')
            return redirect("/newpost")
        if not blog_title:
            msg_title = "There is no title"
            flash(msg_title,'title')
            return redirect("/newpost?blog_body=" + blog_body)
        if not blog_body:
            msg_body = "There is no body"
            flash(msg_body,'body')
            return redirect("/newpost?blog_title=" + blog_title)
        else:
            username = session.get("username")
            user = User.query.filter_by(username=username).first() #get user_id based on logged in user
            blog = Blog(blog_title,blog_body,user)
            db.session.add(blog)
            db.session.commit()
            new_id = db.session.query(db.func.max(Blog.id)).scalar()

            return redirect("/blog?postid=" + str(new_id))     

    if request.method == "GET":
        blog_body = request.args.get("blog_body")
        blog_title = request.args.get("blog_title")

        if blog_body:
            blog_body.strip()
        if blog_title:
            blog_title.strip()

        if blog_body and blog_title:
            return render_template("newpost.html")
        elif blog_title:
            return render_template("newpost.html",blog_title=blog_title)
        elif blog_body:
            return render_template("newpost.html",blog_body=blog_body)


    return render_template("newpost.html")

@app.route("/",methods = ["GET","POST"])
def index():
   
    users = User.query.all()
    print(users)

    return render_template("index.html",title="Home",users=users)


if __name__ == "__main__":
	app.run()