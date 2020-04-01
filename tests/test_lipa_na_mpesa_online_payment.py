import os

from mpesa_sdk.helpers import utils
from tests.base import BaseTest


class TestLipaNaMpesaOnlinePayment(BaseTest):
    def test_successful_lipa_na_mpesa_online_payment_api(self):
        data = {
          "BusinessShortCode": os.environ.get("SAFARICOM_PAY_BILL"),
          "Password": "",
          "Timestamp": "",
          "TransactionType": "CustomerPayBillOnline",
          "Amount": "",
          "PartyA": "",
          "PartyB": "",
          "PhoneNumber": "",
          "CallBackURL": "",
          "AccountReference": "",
          "TransactionDesc": ""
        }
        body, status_code = self.instance.lipa_na_mpesa_online_payment(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseDescription" in body
        assert "ResponseCode" in body
        assert "CustomerMessage" in body
        assert status_code == 200
