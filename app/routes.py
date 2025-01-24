from flask import Blueprint, make_response, render_template, request, redirect, jsonify, current_app
import uuid
from .models import retrieve_all_posts, store_post, get_post, delete_post
from .helpers import userSignedIn

bp = Blueprint('main', __name__)

@bp.route('/')
def home():     
    
    print("app/routes.py --> home()")
           
    # Verify Firebase auth.
    verified = userSignedIn()
    
    raw_posts = retrieve_all_posts()
    
    rendered_posts = list()
    
    for raw_post in raw_posts:
        
        id = raw_post.id
        raw_post = raw_post.to_dict()
        
        if raw_post["post"] == None:
            post = "Empty Post"
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
    
# create new post
@bp.route("/post", methods=["GET"])
def post():
    
    print("app/routes.py --> post()")
    verified = userSignedIn()        
        
    if verified.get('authenticated'):
        # "Authenticated GET"
        edit = request.args.get("edit")
        post_id = str(uuid.uuid4())
        ret_post = {"title": "","post": "", "private": "", "post_id": post_id}
        return render_template("post.html", post=ret_post, show_alert=False, user_data=verified["claims"], edit=edit)
    else:
        # "Unauthenticated GET response"
        return redirect("/")
    
# edit/read post
@bp.route("/post/<post_id>", methods=["GET", "POST"])
def view_post(post_id):
    
    print("app/routes.py --> view_post()")
    
    verified = userSignedIn()
    authenticated = verified.get('authenticated')
    
    print(f"/post/{post_id}. Authenticated: {authenticated}")
    
    if request.method == "POST" and verified.get('authenticated'):        
        # POST
        print("/post 'POST' request")
        # get the title and post from the form submission
        title = request.form.get("title")
        post = request.form.get("post")
        private = request.form.get("private")
        user_id = verified["claims"]["user_id"]
        post_id = request.form.get("post_id", None)
        
        if private == "on":
            private = True
        else:
            private = False
            
        ret_post = {"post": post, "title": title, "private": private, "post_id": post_id}
        
        show_alert = title == "" or post == ""
        
        if not show_alert:
            store_post({"title": title, "post": post, "private": private, "post_id": post_id}, user_id)
          
        # return render_template("post.html", post=ret_post, show_alert=show_alert, user_data=verified["claims"], edit=show_alert)
        
        return jsonify({"post": ret_post, "show_alert": show_alert, "edit": show_alert})
        
    else:
    
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
        
        # print(f"Edit: {edit}")
        
        if private and authenticated:
            # return render_template("post.html", post=complete_post, show_alert=None, user_data=verified["claims"], edit=edit)
            return jsonify({"post": complete_post, "show_alert": False, "user_data": verified["claims"], "edit": edit})
        else:
            # return render_template("post.html", post=complete_post, show_alert=None, user_data=verified["claims"], edit=edit)
            return jsonify({"post": complete_post, "show_alert": False, "user_data": verified["claims"], "edit": edit})
      
@bp.route("/post/<post_id>/delete", methods=["DELETE"])
def delete_post_api(post_id):
    
    print("app/routes.py --> delete_post_api()")
    
    verified = userSignedIn()
        
    if request.method == "DELETE" and verified.get("authenticated"):
        print(f"DELETING post_id: {post_id}")
        deleted_post = delete_post(post_id)
        return {"post_id": post_id, "deleted": True, "message": deleted_post}

    else:
        return {"message": "Could not delete"}