from extensions.my_firestore import db
from google.cloud import firestore
import argparse

def retrieve_posts(posts_collection_name):
    
    print(f"extensions/move_posts_to_new_collection.py --> retrieve_all_posts({posts_collection_name})")
    
    print(f"posts_collection_name: {posts_collection_name}")
    
    
    posts_ref = db.collection(posts_collection_name)
    query = posts_ref.order_by("date", direction=firestore.Query.DESCENDING)
    posts = query.stream()
    
    return posts

def populate_posts(posts, posts_collection_name):   
    
    print("populate_blogs()")

    batch = db.batch()
        
    try:
        
        for post in posts:   
            id = post.id         
            post = post.to_dict()
                    
            document = db.collection(posts_collection_name).document(id)
            batch.set(document, post)
            
        batch.commit()
    
        return "populated successfully"
    
    except Exception as e:
        error = f"Exception: {e}"
        print(error)
        return error
    
def main():
    
    parser = argparse.ArgumentParser(description="get collection names.")
    
    parser.add_argument("--from_coll", type=str, required=True)
    parser.add_argument("--to_coll", type=str, required=True)
    
    args = parser.parse_args()
    
    posts = retrieve_posts(args.from_coll)
    populate_posts(posts, args.to_coll)
    
        
if __name__ == "__main__":
    main()
