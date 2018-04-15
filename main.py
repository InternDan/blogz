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

    def __repr__(self):
        return "<Blog(title='%s', body='%s')>" % (self.title, self.body)

@app.route("/blog")
def blog():
    blogs = Blog.query.all()

    if request.method == "GET" and request.args.get("id"):
        blog_id = request.args.get("id")
        blogs = Blog.query.get(blog_id)
        if blogs:
            return render_template("blog.html",title="Build a Blog!",blog=blogs)

    elif blogs:
        blogs = Blog.query.all()
        if blogs:
            return render_template("blogs.html",title="Build a Blog!",blogs=blogs)

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
            blog = Blog(blog_title,blog_body)
            db.session.add(blog)
            db.session.commit()
            new_id = db.session.query(db.func.max(Blog.id)).scalar()
            print(new_id)

            return redirect("/blog?id=" + str(new_id))     

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
   
    blogs = Blog.query.all()

    if blogs:
        return redirect("/blog")

    return render_template("blogs.html",title="Build a Blog!",blogs=blogs)


if __name__ == "__main__":
	app.run()