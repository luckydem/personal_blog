from google.cloud import datastore
import requests
import json
import datetime

def populate_blogs():    

    client = datastore.Client()

    upload_list = list()

    with open("../data/blog_entries.json", 'r') as file:
        data = json.load(file)
        
    try:
        
        for i in range(len(data)):
            e = data[i]
            
            e["date"] = datetime.datetime.fromisoformat(e["date"])
            
            e["image"] = e.get("image", get_unsplash_image())
                    
            entry = datastore.Entity(client.key("post"))
            entry.update(e)
            upload_list.append(entry)
            
        client.put_multi(upload_list)
    
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