"""# auth.py
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
import os

# OAuth Setup
oauth = OAuth()

def init_oauth(app: FastAPI):
    oauth = OAuth()
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile", "token_endpoint_auth_method": "client_secret_post"},
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    )

"""