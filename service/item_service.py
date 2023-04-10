
from firebase_admin import credentials
from firebase_admin import initialize_app
from firebase_admin import firestore

from model.item_model import ItemModel
from utils.constants import FIRESTORE_PROJECT_ID


cred = credentials.ApplicationDefault()
initialize_app(cred, {
    'projectId': FIRESTORE_PROJECT_ID,
})


db = firestore.client()


def get_items():
    doc_ref = db.collection(u'items').get()
    docs = []
    for doc in doc_ref:
        docs.append(doc.to_dict())

    return docs


def save_item(id: str):
    doc_ref = db.collection(u'items').document(id)
    doc_ref.set({"item_id": id})
    return True


def remove_item(item_id: str):
    db.collection(u'items').document(item_id).delete()
    return True