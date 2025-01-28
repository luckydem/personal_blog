from extensions.my_firestore import db
import requests
import json
import datetime
import uuid
from config import config


# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

# db = firestore.Client(project="my-personal-blog-cs50")

# doc_ref = db.collection("users").document("demianhauptle")
# doc_ref.set({"first": "Demian", "last": "Hauptle", "born": 1985})



def populate_blogs():   
    
    print("populate_blogs()")

    batch = db.batch()
    
    post_collection = config["development"].POSTS
    
    # db.collection("posts").document("MLOTHzQFEXRQHa4GpMLv2ywiWVv2")

    # upload_list = list()

    with open("sample_data/blog_entries.json", 'r') as file:
        data = json.load(file)
        
    try:
        
        for i in range(len(data)):            
            post = data[i]
            id = str(uuid.uuid4())
            # print(f"post {i+1}: id: {id}. title: {post["title"]}")
            
            
            post["date"] = datetime.datetime.fromisoformat(post["date"])
            
            post["image"] = post.get("image", get_unsplash_image())
                    
            document = db.collection(post_collection).document(id)
            batch.set(document, post)
            
        batch.commit()
    
        return "populated successfully"
    
    except Exception as e:
        error = f"Exception: {e}"
        print(error)
        return error
    
def get_unsplash_image():
    
    # print("get_unsplash_image()")
    
    url = "https://api.unsplash.com/photos/random?client_id=_Qmfzy6iu5ozPXrKglsJjwlk-Yics0-xxEO-N9G-ogI"
    headers = {
        "Accept-Version": "v1"
    }
    
    response = requests.get(
        url=url,
        headers=headers        
    )
    
    # print(response.json())
    
    if response.status_code == 200:    
        # print(response.json()["urls"]["small"])
        return response.json()["urls"]["small"]
    else:
        print(f"Error: response code: {response.status_code}, Message: {response.text}")
        return None
    
# get_unsplash_image()
populate_blogs()
