# oauth_provider.py
from authlib.integrations.flask_client import OAuth
from decouple import config
oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=config("client_id", cast=str),
    client_secret=config("client_secret", cast=str),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid profile email',
        'redirect_uri': 'http://127.0.0.1:5000/auth'
    }
)

