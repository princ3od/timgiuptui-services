import os
import json
import base64
from google.cloud.firestore import Client
from firebase_admin import firestore, credentials, initialize_app
from constants import LOCAL_FIRESTORE_CREDENTIAL_PATH


if not os.environ.get("FIREBASE_CRED"):
    firebase_credentials = credentials.Certificate(LOCAL_FIRESTORE_CREDENTIAL_PATH)
else:
    decodedkey = base64.b64decode(os.environ["FIREBASE_CRED"]).decode("ascii")
    cred_dict = json.loads(decodedkey)
    firebase_credentials = credentials.Certificate(cred_dict)

initialize_app(firebase_credentials)
firestore_db: Client = firestore.client()
