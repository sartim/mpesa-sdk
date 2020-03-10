import os

from dotenv import load_dotenv
from mpesa_sdk.gateway import oauth_generate_token, Mpesa

load_dotenv()


class BaseTest:
    @classmethod
    def setup_class(cls):
        access_token = oauth_generate_token(
            consumer_key=os.environ.get("CONSUMER_KEY"),
            consumer_secret=os.environ.get("CONSUMER_SECRET"),
            grant_type="client_credentials",
            env="sandbox")
        cls.instance = Mpesa(access_token, env="sandbox")
