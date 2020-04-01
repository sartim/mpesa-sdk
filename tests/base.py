import os

from dotenv import load_dotenv
from mpesa_sdk.gateway import oauth_generate_token, Mpesa

load_dotenv()


class BaseTest:
    @classmethod
    def setup_class(cls):
        cls.consumer_key = os.environ.get("CONSUMER_KEY")
        cls.consumer_secret = os.environ.get("CONSUMER_SECRET")
        access_token = oauth_generate_token(
            consumer_key=cls.consumer_key,
            consumer_secret=cls.consumer_secret,
            grant_type="client_credentials",
            env="sandbox")
        cls.instance = Mpesa(access_token, env="sandbox")
