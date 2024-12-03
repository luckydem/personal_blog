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
            "post": post["post"],
            "title" : post["title"]
        }
    )
    
    datastore_client.put(entity)
    
def retrieve_posts():
    query = datastore_client.query(kind="post")
    query.order = ["-date"]
    
    posts = list(query.fetch())
    
    # print(posts)
    
    return posts

app = Flask(__name__)


@app.route('/')
def home():
    raw_posts = retrieve_posts()
    
    rendered_posts = list()
    
    for raw_post in raw_posts:
        if raw_post["post"] == None:
            post = "Empty Post"
        else:
            post = raw_post["post"]  
              
        title = raw_post.get("title", "Empty Title")
        
        rendered_posts.append({"title": title, "post": post, "id": raw_post.id})
    
    return render_template("index.html", posts=rendered_posts)

@app.route("/post", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # get the title and post from the form submission
        title = request.form.get("title")
        post = request.form.get("post")
        
        store_post({"title": title, "post": post})
        
        return redirect("/")
    else:
        return render_template("create_post.html")
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)