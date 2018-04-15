from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "weioha8e8aehfaklsdfnaueh"
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route("/blog")
def blog():
    blogs = Blog.query.all()

    if blogs:
        return render_template("blogs.html",title="Build a Blog!",blogs=blogs)

@app.route("/newpost",methods = ["POST","GET"])
def new_post():
    if request.method == "POST":
        blog_title = request.form["title"]
        blog_body = request.form["body"]

        if not blog_title and not blog_body:
            msg_title = "There is no title"
            msg_body = "There is no body"
            return redirect("/newpost?msg_title=" +  msg_title + "&msg_body=" + msg_body)
        if not blog_title:
            msg_title = "There is no title"
            return redirect("/newpost?msg_title=" +  msg_title + "&blog_body=" + blog_body)
        if not blog_body:
            msg_body = "There is no body"
            return redirect("/newpost?msg_body=" + msg_body + "&blog_title=" + blog_title)
        else:
            blog = Blog(blog_title,blog_body)
            db.session.add(blog)
            db.session.commit()

            return redirect("/blog")     

    if request.method == "GET":
        msg_title = request.args.get("msg_title")
        msg_body = request.args.get("msg_body")

        blog_body = request.args.get("blog_body")
        blog_title = request.args.get("blog_title")

        if msg_title and msg_body:
            return render_template("newpost.html",msg_title=msg_title,msg_body=msg_body)
        elif msg_title:
            return render_template("newpost.html",msg_title=msg_title,blog_body=blog_body)
        elif msg_body:
            return render_template("newpost.html",msg_body=msg_body,blog_title=blog_title)


    return render_template("newpost.html")

@app.route("/",methods = ["GET","POST"])
def index():
   
    blogs = Blog.query.all()

    if blogs:
        return redirect("/blog")

    return render_template("blogs.html",title="Build a Blog!",blogs=blogs)


if __name__ == "__main__":
	app.run()