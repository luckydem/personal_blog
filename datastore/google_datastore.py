from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def store_post(post, userId):
    entity = datastore.Entity(key=datastore_client.key("post"), exclude_from_indexes=("post",))
    entity.update(
        {
            "status": post["status"],
            "date": datetime.datetime.now(),
            "post": post["post"],
            "title": post["title"],
            "userId": userId
        }
    )
    
    datastore_client.put(entity)
    
def retrieve_posts():
    query = datastore_client.query(kind="post")
    query.keys_only()
    has_posts = len(list(query.fetch(limit=1))) > 0
    if not has_posts:
        return []
    
    query = datastore_client.query(kind="post")
    query.order = ["-date"]
    
    posts = list(query.fetch())
    
    # print(posts)
    
    return posts

def retrieve_user(user_id):
    query = datastore_client.query(kind="user")
    query.add_filter(filter=datastore.query.PropertyFilter("user_id", "=", user_id))
    
    user = len(list(query.fetch())) > 0
    
    return user
    