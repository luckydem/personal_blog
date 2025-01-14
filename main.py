from flask import Flask, render_template, request, redirect, url_for, make_response
from google.auth.transport import requests
from extensions.my_firestore import store_post, retrieve_all_posts, retrieve_user, get_post, delete_post
import google.oauth2.id_token

app = Flask(__name__)

def userSignedIn():
    id_token = request.cookies.get("token")
    
    # print(f"id_token: {id_token}")
    
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
    
    print(f"authenticated: {authenticated}")
    
            
    return {"error_message": error_message, "claims" : claims, "authenticated": authenticated}

# Home page. If logged in, display both public and private posts as well as edit icons
firebase_request_adapter = requests.Request()
@app.route('/')
def home():
    # Verify Firebase auth.
    verified = userSignedIn()
    
    raw_posts = retrieve_all_posts()
    
    rendered_posts = list()
    
    for raw_post in raw_posts:
        
        id = raw_post.id
        raw_post = raw_post.to_dict()
        
        if raw_post["post"] == None:
            post = "Empty Post"
        # elif len(raw_post["post"]) > 250:
        #     post = raw_post["post"][:250] + "...[truncated]"
        else: post = raw_post["post"]
              
        title = raw_post.get("title", "Empty Title")
        date = raw_post.get("date").strftime("%a, %d %b %Y")
        private = raw_post.get("private", "false")
        image = raw_post.get("image", "")
        
        # print(f"Title: {title}")
        # print(f"Image: {image}")
        
        post_ready = {"title": title, "post": post, "id": id, "date": date, "private": private, "image": image}
        
        if private and verified.get("authenticated"):
            # print(f"private: {private}, verified: {verified.get("authenticated")}")
            rendered_posts.append(post_ready)
        elif not private:
            rendered_posts.append(post_ready)
        
    resp = make_response(render_template("index.html", user_data=verified["claims"], posts=rendered_posts))
        
    if verified.get('authenticated'):
        return resp
    else:        
        resp.delete_cookie(key='token')
        return resp

# submit post page
@app.route("/post", methods=["GET", "POST"])
def post():
    
    print("Navigating to /post")
    verified = userSignedIn()
    
    if request.method == "POST" and verified.get('authenticated'):        
        # POST
        print("/post 'POST' request")
        # get the title and post from the form submission
        title = request.form.get("title")
        post = request.form.get("post")
        private = request.form.get("private")
        user_id = verified["claims"]["user_id"]
        post_id = request.form.get("post_id", None)
        
        if not post_id == "":
            print(f"post_id: {post_id}")
        
        print(f"Post private: {private}")        
        print(f"title: {title}")
        print(f"post: {post}")
        
        if private == "on":
                private_ret = "checked"
                private = True
        else:
            private_ret = ""
            private = False
            
        ret_post = {"post": post, "title": title, "private": private_ret}
        
        show_alert = title == "" or post == ""
        print(f"show_alert Status: {show_alert}")
        
        if not show_alert:
            store_post({"title": title, "post": post, "private": private, "post_id": post_id}, user_id)
          
        resp = make_response(render_template("post.html", post=ret_post, show_alert=show_alert, user_data=verified["claims"], edit=show_alert))
        
    elif request.method == "GET" and verified.get('authenticated'):
        # "Authenticated GET"
        edit = request.args.get("edit")
        ret_post = {"title": "","post": "", "private": ""}
        resp = make_response(render_template("post.html", post=ret_post, show_alert=False, user_data=verified["claims"], edit=edit))
    else:
        # "Unauthenticated GET response"
        resp = make_response(redirect("/"))
        
    return resp
    
# edit/read post
@app.route("/post/<post_id>", methods=["GET"])
def view_post(post_id):
    
    verified = userSignedIn()
    authenticated = verified.get('authenticated')
    
    print(f"/post/{post_id}. Authenticated: {authenticated}")
        
    complete_post = get_post(post_id)
    
    post_id = complete_post.id
    complete_post = complete_post.to_dict()
    
    complete_post["post_id"] = post_id
    
    edit = False
    private = False
    
    if (complete_post["private"]):
        complete_post["private"] = "checked"
        private = True
    else:
        complete_post["private"] = ""

    if request.args.get("edit") == "true" and authenticated:
        edit = True        
    
    print(f"Edit: {edit}")
    
    if private and authenticated:
        return render_template("post.html", post=complete_post, show_alert=None, user_data=verified["claims"], edit=edit)
    else:
        return render_template("post.html", post=complete_post, show_alert=None, user_data=verified["claims"], edit=edit)
    
 
    
@app.route("/post/<int:post_id>/delete", methods=["POST"])
def dele_post(post_id):
    verified = userSignedIn()
    
    print(f"DELETE. post_id: {post_id}")
    
    if request.method == "POST" and verified.get("authenticated"):
        delete_post(post_id)

    return redirect("/")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)