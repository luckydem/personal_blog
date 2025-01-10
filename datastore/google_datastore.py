from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def store_post(post, userId):
    
    post_id = post.get("post_id", "")
        
    if not post_id == "":    
        print(f"POST ID: {post_id}")    
        key = datastore_client.key("post", int(post_id))
    else:
        key = datastore_client.key("post")
        
    entity = datastore.Entity(key=key, exclude_from_indexes=("post",))   
    entity.update(
        {
            "private": post["private"],
            "date": datetime.datetime.now(),
            "post": post["post"],
            "title": post["title"],
            "userId": userId
        }
    )
    
    datastore_client.put(entity)
    
def datastore_query_kinds_exist(kind):
    query = datastore_client.query(kind=kind)
    query.keys_only()
    has_posts = len(list(query.fetch(limit=1))) > 0
    
    if not has_posts:
        return False
    else:
        return True
    
    
def retrieve_all_posts():
    # query = datastore_client.query(kind="post")
    # query.keys_only()
    # has_posts = len(list(query.fetch(limit=1))) > 0
    # if not has_posts:
    #     return []
    
    if not datastore_query_kinds_exist("post"):
        return []
    
    query = datastore_client.query(kind="post")
    query.order = ["-date"]
    
    posts = list(query.fetch())
    
    # print(posts)
    
    return posts

def get_post(post_id):
    
    key = datastore_client.key("post", int(post_id))
    post = datastore_client.get(key)
        
    return post
        
def upsert_post(post_id, data):
    
    try:
        post = datastore.Entity(datastore_client.key("post", int(post_id)))
    
        post.update(
            data
        )
        res = "success"
        
    except ValueError as e:
        error_message = str(e)
    
    return {"message": res, "error": error_message}

def delete_post(post_id):
    datastore_client.delete(datastore_client.key("post", int(post_id)))
    

def retrieve_user(user_id):
    query = datastore_client.query(kind="user")
    query.add_filter(filter=datastore.query.PropertyFilter("user_id", "=", user_id))
    
    user = len(list(query.fetch())) > 0
    
    return user
    