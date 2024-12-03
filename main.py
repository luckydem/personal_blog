from flask import Flask, render_template, request, redirect, url_for
from google.cloud import datastore
import datetime


datastore_client = datastore.Client()

def store_post(post):
    entity = datastore.Entity(key=datastore_client.key("post"))
    entity.update(
        {
            "status": "public",
            "date": datetime.datetime.now(),
            "post": post
        }
    )
    
    datastore_client.put(entity)
    
def retrieve_posts():
    query = datastore_client.query(kind="post")
    query.order = ["-date"]
    
    posts = list(query.fetch())
    
    print(posts)
    
    return posts

app = Flask(__name__)


@app.route('/')
def home():
    posts = retrieve_posts()
    
    return render_template("index.html", posts=posts)

@app.route("/post", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # get the post from the form submission
        post = request.form.get("post")
        print(post)
        
        store_post(post)
        
        return redirect("/")
    else:
        return render_template("create_post.html")
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)