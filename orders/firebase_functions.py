from .firebase import firebase_db

def save_item_to_firebase(item):
    data = {
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "price": float(item.price),
        "available": item.available,
        "category": item.category.name if item.category else None,
        "created_at": item.created_at.isoformat(),
        "image_url": item.image_url
    }

    # Save under 'items/{item_id}'
    firebase_db.child('items').child(str(item.id)).set(data)
    print(f"🔥 Item {item.name} saved to Firebase Realtime DB")
