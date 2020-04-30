import unittest

from tests.base import BaseTest


class TestStkPush(BaseTest):
    def test_stk_push(self):
        amount = 10  # You can change this to any amount in KSH
        data = {
            "BusinessShortCode": self.short_code,
            "Password": self.password,
            "Timestamp": self.current_timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": self.mobile_number,
            "PartyB": self.short_code,
            "PhoneNumber": self.mobile_number,
            "CallBackURL": self.callback_url,
            "AccountReference": self.order_id,
            "TransactionDesc": "CustomerBuyGoodsOnline"
        }
        body, status_code = self.instance.lipa_na_mpesa_online_payment(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseDescription" in body
        assert "ResponseCode" in body
        assert "CustomerMessage" in body
        assert status_code == 200

        data = {
            "BusinessShortCode": self.short_code,
            "Password": self.password,
            "Timestamp": self.current_timestamp,
            "CheckoutRequestID": body["CheckoutRequestID"]
        }
        body, status_code = self.instance.lipa_na_mpesa_online_query(data)

        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseCode" in body
        assert "ResultDesc" in body
        assert "ResponseDescription" in body
        assert "ResultCode" in body
        assert status_code == 200
