from flask import Flask, render_template, request, redirect, url_for, make_response
from google.auth.transport import requests
from datastore.google_datastore import store_post, retrieve_posts, retrieve_user
import google.oauth2.id_token

app = Flask(__name__)

def userSignedIn():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    authenticated = False
    
    if id_token:        
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )
            
            authenticated = retrieve_user(claims.get('user_id'))  
                                            
        except ValueError as exc:
            error_message = str(exc)   
    
    
            
    return {"error_message": error_message, "claims" : claims, "authenticated": authenticated}

# Home page. If logged in, display both public and private posts as well as edit icons
firebase_request_adapter = requests.Request()
@app.route('/')
def home():
    # Verify Firebase auth.
    verified = userSignedIn()
    
    raw_posts = retrieve_posts()
    
    rendered_posts = list()
    
    for raw_post in raw_posts:
        if raw_post["post"] == None:
            post = "Empty Post"
        else:
            post = raw_post["post"]  
              
        title = raw_post.get("title", "Empty Title")
        date = raw_post.get("date").strftime("%a, %d %b %Y")
        status = raw_post.get("status", "private")
        
        if status == "public":
            rendered_posts.append({"title": title, "post": post, "id": raw_post.id, "date": date, "status": status})
        elif verified.get('authenticated'):
            rendered_posts.append({"title": title, "post": post, "id": raw_post.id, "date": date, "status": status})
        
            
    
    if verified.get('authenticated'):
        return render_template("index.html", user_data=verified["claims"], posts=rendered_posts)
    else:
        resp = make_response(render_template("index.html", user_data=None, posts=rendered_posts))
        resp.delete_cookie(key='token')
        return resp

# submit post page
@app.route("/post", methods=["GET", "POST"])
def post():
    
    verified = userSignedIn()
    
    # print(f"Authenticated: {verified.get('authenticated')}")
    
    if request.method == "POST" and verified.get('authenticated'):
        # get the title and post from the form submission
        title = request.form.get("title")
        post = request.form.get("post")
        private = request.form.get("private")
        userId = verified["claims"]["user_id"]
        
        print(f"Post status: {private}")
        if private:
            status = "private"
        else: 
            status = "public"
        
        # print(f"title: {title}")
        # print(f"post: {post}")
        
        if title != "" and post != "":            
            store_post({"title": title, "post": post, "status": status}, userId)
            return redirect("/")
        else:            
            showAlert = title != "" or post != ""
            return render_template("post.html", title=title, post=post, showAlert=showAlert)
    elif verified.get('authenticated'):
        return render_template("post.html", showAlert = False, user_data = verified["claims"])
    else:
        resp = make_response(redirect("/"))
        resp.delete_cookie(key='token')
        return resp
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)