from flask import Flask, request, redirect, render_template

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route("/blog")
def blog()
    blogs = Blogs.query.all()

    if blogs:
        return render_template("blogs.html",title="Your blog posts",blog=blogs)

@app.route("/newpost")
def new_post():
     if request.method == "POST":
        blog_title = request.form["title"]
        blog_content = request.form["content"]

        blog = Blog(blog_title,blog_content)
        db.session.add(blog)
        db.session.commit()

    return redirect("/")

@app.route("/",methods = ["GET","POST"])
def index():
   
    blogs = Blogs.query.all()

    if blogs:
        return redirect("/blog")

    return render_template("blogs.html",title="Build a Blog!",blog=blogs)


if __name__ == "__main__":
	app.run()