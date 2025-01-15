from google.cloud import firestore
import datetime

db = firestore.Client(project="my-personal-blog-cs50")

def store_post(post, userId):
    
    post_id = post.get("post_id")
    
    print(f"post_id: {post_id}")
    
    if post_id:        
        entity = db.collection("posts").document(post_id)
    else:
        entity = db.collection("posts").document()
        
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
    # potentially at this point, we could retrieve all posts except private posts when 
    # user is not logged in...
    
    # query = db.query(kind="post")
    # query.keys_only()
    # has_posts = len(list(query.fetch(limit=1))) > 0
    # if not has_posts:
    #     return []
    
    posts_ref = db.collection("posts")
    query = posts_ref.order_by("date", direction=firestore.Query.DESCENDING)
    posts = query.stream()
    
    return posts

def get_post(post_id):
    
    post_ref = db.collection("posts").document(post_id)
    
    post = post_ref.get()
    
    if post.exists:
        return post
    else:
        print(f"post with id: '{post_id}' doesn't exist")

def delete_post(post_id):
    db.collection("posts").document(post_id).delete()
    

def create_user(user_id, email, slug):
    user_ref = db.collection("users").document(user_id)
    user_ref.set(
        {
            "email": email,
            "slug": slug
        }
    )

def retrieve_user(user_id):
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()
    
    return user
    