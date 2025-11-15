import requests

FIREBASE_URL = "https://canteen-app-61545-default-rtdb.firebaseio.com/"

def send_to_firebase(path, data):
    """
    Send data to Firebase Realtime Database using POST method.
    Example path: 'items', 'orders', 'payments'
    """
    try:
        url = f"{FIREBASE_URL}{path}.json"
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print("Firebase Error:", e)
        return None
