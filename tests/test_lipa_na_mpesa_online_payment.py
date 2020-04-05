import unittest

from tests.base import BaseTest


class TestLipaNaMpesaOnlinePayment(BaseTest):
    @unittest.skip("Test with legit values")
    def test_successful_lipa_na_mpesa_online_payment_api(self):
        amount = 10
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
            "AccountReference": "You are being charged {} for the item {}".format(
                amount, "Test"),
            "TransactionDesc": "CustomerBuyGoodsOnline"
        }
        body, status_code = self.instance.lipa_na_mpesa_online_payment(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseDescription" in body
        assert "ResponseCode" in body
        assert "CustomerMessage" in body
        assert status_code == 200
