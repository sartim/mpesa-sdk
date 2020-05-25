from unittest.mock import MagicMock

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
        result = {
            "MerchantRequestID": "14938-14045528-1",
            "CheckoutRequestID": "ws_CO_300420201828468847",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing"
        }
        self.instance.lipa_na_mpesa_online_payment = MagicMock(
            return_value=(result, 200))
        body, status_code = self.instance.lipa_na_mpesa_online_payment(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseDescription" in body
        assert "ResponseCode" in body
        assert "CustomerMessage" in body
        assert status_code == 200

    def test_stk_confirm(self):
        checkout_request_id = "ws_CO_300420201835238048"
        data = {
            "BusinessShortCode": self.short_code,
            "Password": self.password,
            "Timestamp": self.current_timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        result = {
            "ResponseCode": "0",
            "ResponseDescription": "The service request has been accepted successfully",
            "MerchantRequestID": "15777-13928452-1",
            "CheckoutRequestID": "ws_CO_300420201835238048",
            "ResultCode": "0",
            "ResultDesc": "The service request is processed successfully."
        }
        self.instance.lipa_na_mpesa_online_query = MagicMock(
            return_value=(result, 200))
        body, status_code = self.instance.lipa_na_mpesa_online_query(data)
        assert "MerchantRequestID" in body
        assert "CheckoutRequestID" in body
        assert "ResponseCode" in body
        assert "ResultDesc" in body
        assert "ResponseDescription" in body
        assert "ResultCode" in body
        assert status_code == 200
