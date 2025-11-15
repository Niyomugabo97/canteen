import os
import firebase_admin
from firebase_admin import credentials, db

# Full path ya JSON key yawe
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "canteen_project", "canteen-app-61545-firebase-adminsdk-fbsvc-696f45b0d2.json")

# Initialize Firebase
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://canteen-app-61545-default-rtdb.firebaseio.com/'
})

# Reference to root
firebase_db = db.reference('/')
