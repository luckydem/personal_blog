from google.cloud import firestore
from config import Config

# db = None

# def initialize_firestore(project_name):
#     print(f"extensions/my_firestore.py --> initialize_firestore({project_name})")
#     return firestore.Client(project=project_name)

# def set_firestore_client(project_name):
#     print(f"extensions/my_firestore.py --> set_firestore_client({project_name})")
#     global db
#     db = initialize_firestore(project_name)
#     print(f"extensions/my_firestore.py --> Firestore client initialized with project: {project_name}") 



db = firestore.Client(Config.FIRESTORE_PROJECT)