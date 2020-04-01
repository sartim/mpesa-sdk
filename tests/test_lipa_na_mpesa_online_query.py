import os
import uuid

from mpesa_sdk.helpers import utils
from tests.base import BaseTest


class TestLipaNaMpesaOnlineQuery(BaseTest):
    def test_successful_lipa_na_mpesa_online_query(self):
        short_code = os.environ.get("SAFARICOM_SHORT_CODE")
        current_timestamp =  utils.current_timestamp
        password = utils.encode_string(
            short_code+self.consumer_key+current_timestamp)
        data = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": current_timestamp,
            "CheckoutRequestID": str(uuid.uuid4())
        }
        body, status_code = self.instance.lipa_na_mpesa_online_query(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseCode" in body
        assert "ResultDesc" in body
        assert "ResponseDescription" in body
        assert "ResultCode" in body
        assert status_code == 200
