import datetime
import os

from dotenv import load_dotenv
from mpesa_sdk.gateway import oauth_generate_token, Mpesa
from mpesa_sdk.helpers import utils

load_dotenv()


class BaseTest:
    @classmethod
    def setup_class(cls):
        current_date_time = datetime.datetime.today()
        cls.consumer_key = os.environ.get("CONSUMER_KEY")
        cls.consumer_secret = os.environ.get("CONSUMER_SECRET")
        cls.short_code = int(os.environ.get("SAFARICOM_SHORT_CODE"))
        cls.mobile_number = os.environ.get("SAFARICOM_TEST_MOBILE_NUMBER")
        cls.current_timestamp = str(utils.convert_datetime_to_int(current_date_time))
        cls.callback_url = os.environ.get("SAFARICOM_CALL_BACK_URL")
        cls.password = utils.encode_string(
            str(cls.short_code) + cls.consumer_key + str(cls.current_timestamp))\
            .decode()
        result, status_code = oauth_generate_token(
            consumer_key=cls.consumer_key,
            consumer_secret=cls.consumer_secret,
            grant_type="client_credentials",
            env="sandbox")
        cls.instance = Mpesa(result["access_token"], env="sandbox")
