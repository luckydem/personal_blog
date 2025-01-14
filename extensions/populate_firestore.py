from google.cloud import firestore
import requests
import json
import datetime


# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.

# db = firestore.Client(project="my-personal-blog-cs50")

# doc_ref = db.collection("users").document("demianhauptle")
# doc_ref.set({"first": "Demian", "last": "Hauptle", "born": 1985})

def populate_blogs():    

    db = firestore.Client()
    batch = db.batch()
    
    # db.collection("posts").document("MLOTHzQFEXRQHa4GpMLv2ywiWVv2")

    # upload_list = list()

    with open("../data/blog_entries.json", 'r') as file:
        data = json.load(file)
        
    try:
        
        for i in range(len(data)):
            post = data[i]
            
            post["date"] = datetime.datetime.fromisoformat(post["date"])
            
            post["image"] = post.get("image", get_unsplash_image())
                    
            document = db.collection("posts").document()
            batch.set(document, post)
            
        batch.commit()
    
        return "populated successfully"
    
    except Exception as e:
        error = f"Exception: {e}"
        print(error)
        return error
    
def get_unsplash_image():
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
        return response.json()["urls"]["small"]
    else:
        print(response.status_code)
        return None
    

populate_blogs()
