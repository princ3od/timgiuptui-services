import base64
import json
import os

from constants import LOCAL_FIRESTORE_CREDENTIAL_PATH
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore import Client

if not os.environ.get("FIREBASE_CRED"):
    firebase_credentials = credentials.Certificate(LOCAL_FIRESTORE_CREDENTIAL_PATH)
else:
    decodedkey = base64.b64decode(os.environ["FIREBASE_CRED"]).decode("ascii")
    cred_dict = json.loads(decodedkey)
    firebase_credentials = credentials.Certificate(cred_dict)

initialize_app(firebase_credentials)
firestore_db: Client = firestore.client()
