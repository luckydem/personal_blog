from flask import current_app
from google.cloud import firestore
from extensions.my_firestore import db
import datetime
import uuid

def store_post(post, userId):
    
    print("app/models.py --> store_post()")
    
    posts_collection_name = current_app.config.get('POSTS')
    
    post_id = post.get("post_id")
    
    print(f"post_id: {post_id}")
    
    if not post_id:
        post_id = uuid.uuid4()
        
    entity = db.collection(posts_collection_name).document(post_id)
        
    entity.set(
        {
            "private": post["private"],
            "date": datetime.datetime.now(),
            "post": post["post"],
            "title": post["title"],
            "userId": userId
        }
    )
        
def retrieve_all_posts():
    
    print("app/models.py --> retrieve_all_posts()")
    # potentially at this point, we could retrieve all posts except private posts when 
    # user is not logged in...
    
    # query = db.query(kind="post")
    # query.keys_only()
    # has_posts = len(list(query.fetch(limit=1))) > 0
    # if not has_posts:
    #     return []
    posts_collection_name = current_app.config.get('POSTS')
    
    print(f"posts_collection_name: {posts_collection_name}")
    
    
    posts_ref = db.collection(posts_collection_name)
    query = posts_ref.order_by("date", direction=firestore.Query.DESCENDING)
    posts = query.stream()
    
    return posts

def get_post(post_id):
    
    print(f"app/models.py --> get_post({post_id})")
    
    posts_collection_name = current_app.config.get('POSTS')
    
    post_ref = db.collection(posts_collection_name).document(post_id)
    
    post = post_ref.get()
    
    if post.exists:
        return post
    else:
        return {"title": "","post": "", "private": False, "post_id": post_id}

def delete_post(post_id):
    
    print(f"app/models.py --> delete_post({post_id})")
    
    posts_collection_name = current_app.config.get('POSTS')
    return db.collection(posts_collection_name).document(post_id).delete()
    
def create_user(user_id, email, slug):
    
    print(f"app/models.py --> create_user({user_id}, {email}, {slug})")

    
    user_ref = db.collection("users").document(user_id)
    user_ref.set(
        {
            "email": email,
            "slug": slug
        }
    )

def retrieve_user(user_id):
    
    print(f"app/models.py --> retrieve_user({user_id})")
    
    print(f"app/models.py --> db initialized: {db}")
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()
    
    return user
    