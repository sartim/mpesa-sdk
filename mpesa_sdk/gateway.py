#!/usr/bin/python

"""
Mpesa REST API for Python.

All class functions take in keyword arguments (data) and
response returned is a response object from (python requests).
From this object you can retrieve the response parameters
as text or json.
"""

import os
import logging
import base64
import datetime
from datetime import datetime
import requests

from mpesa_sdk import urls

logger = logging.getLogger()


class Mpesa:

    def __init__(self, access_token, env, version="v1", timeout=None):
        self.headers = {"Authorization": "Bearer {}".format(access_token)}
        self.env = env
        self.version = version
        self.timeout = timeout

    def make_request(self, url, payload, method):
        """
        Invoke url and return a python request object.
        :param url:
        :param payload:
        :param method:
        :return response (obj):
        """
        if self.timeout:
            return requests.request(
                method, url, headers=self.headers,
                json=payload,
                timeout=self.timeout)
        else:
            return requests.request(
                method, url, headers=self.headers,
                json=payload)

    def b2b_payment_request(self, data):
        """
        B2B Payment request.
        Mpesa Transaction from one company to another.
        https://developer.safaricom.co.ke/b2b/apis/post/paymentrequest
        :param data:
        :return response (json):
        """
        expected_keys = [
            "Initiator", "SecurityCredential",
            "CommandID", "SenderIdentifierType",
            "RecieverIdentifierType", "Amount",
            "PartyA", "PartyB", "AccountReference",
            "Remarks", "QueueTimeOutURL", "ResultURL", ]
        payload = process_data(expected_keys, data)
        url = urls.get_b2b_payment_request_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning("B2B payment request has not been completed")
        return {"message": "Request was not completed"}, 500

    def b2c_payment_request(self, data):
        """
        B2C Payment Request.
        Mpesa Transaction from company to client.
        https://developer.safaricom.co.ke/b2c/apis/post/paymentrequest
        :param data:
        :return response (json):
        """
        expected_keys = [
            "InitiatorName", "SecurityCredential",
            "CommandID", "Amount", "PartyA",
            "PartyB", "Remarks", "QueueTimeOutURL",
            "ResultURL", "Occasion", ]
        payload = process_data(expected_keys, data)
        url = urls.get_b2c_payment_request_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning("B2C payment request has not been completed")
        return {"message": "Request was not completed"}, 500

    def c2b_register_url(self, data):
        """
        C2B Register Url.
        Use this API to register validation and confirmation URLs on M-Pesa.
        NOTE: This should be registered once. To update the urls registered
        contact Safaricom which will take some time to be propagated.
        https://developer.safaricom.co.ke/c2b/apis/post/registerurl
        :param data:
        :return response (json):
        """
        expected_keys = [
            "ShortCode", "ResponseType",
            "ConfirmationURL", "ValidationURL"]
        payload = process_data(expected_keys, data)
        url = urls.get_c2b_register_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning("C2B register url request has not been completed")
        return {"message": "Request was not completed"}, 500

    def c2b_simulate_transaction(self, data):
        """
        C2B Simulate Transaction.
        Use this API to simulate a C2B transaction.
        https://developer.safaricom.co.ke/c2b/apis/post/simulate
        :param data:
        :return response (json):
        """
        expected_keys = [
            "ShortCode", "Amount", "Msisdn"]
        payload = process_data(expected_keys, data)
        payload["CommandID"] = "CustomerPayBillOnline"
        url = urls.get_c2b_simulate_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning(
            "C2B simulate transaction request has not been completed")
        return {"message": "Request was not completed"}, 500

    def transation_status_request(self, data):
        """
        Transaction Status Request.
        Use this API to check the status of transaction.
        https://developer.safaricom.co.ke/transaction-status/apis/post/query
        :param data:
        :return response (json):
        """
        expected_keys = [
            "Initiator", "SecurityCredential",
            "TransactionID", "PartyA",
            "ResultURL", "QueueTimeOutURL",
            "Remarks", "Occasion"]
        payload = process_data(expected_keys, data)
        payload["CommandID"] = "TransactionStatusQuery"
        payload["IdentifierType"] = "1"
        url = urls.get_transaction_status_url(self.env)
        req = self.make_request(
            url, payload,
            "POST")
        if req:
            return req.json(), req.status_code
        logger.warning("Transaction status request has not been completed")
        return {"message": "Request was not completed"}, 500

    def account_balance_request(self, data):
        """
        Account Balance Request.
        Use this API to enquire the balance on an Mpesa BuyGoods (Till Number).
        https://developer.safaricom.co.ke/account-balance/apis/post/query
        :param data:
        :return response (json):
        """
        expected_keys = [
            "Initiator", "SecurityCredential", "PartyA",
            "Remarks", "QueueTimeOutURL", "ResultURL"]
        payload = process_data(expected_keys, data)
        payload["CommandID"] = "AccountBalance"
        payload["IdentifierType"] = "4"
        url = urls.get_account_balance_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning(
            "Account balance request has not been completed")
        return {"message": "Request was not completed"}, 500

    def reversal_request(self, data):
        """
        Reversal Request.
        Use this API for reversal transaction.
        https://developer.safaricom.co.ke/reversal/apis/post/request
        :param data:
        :return response (json):
        """
        expected_keys = [
            "Initiator", "SecurityCredential",
            "TransactionID", "Amount",
            "ReceiverParty", "ResultURL",
            "QueueTimeOutURL", "Remarks", "Occasion"]
        payload = process_data(expected_keys, data)
        payload["CommandID"] = "TransactionReversal"
        payload["RecieverIdentifierType"] = "4"
        url = urls.get_reversal_request_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            response = req.json()
            return response, req.status_code
        logger.warning("Reversal request has not been completed")
        return {"message": "Request was not completed"}, 500

    def lipa_na_mpesa_online_query(self, data):
        """
        Lipa na M-Pesa online query.
        For Lipa Na M-Pesa online payment using STK Push.
        https://developer.safaricom.co.ke/lipa-na-m-pesa-online/
            apis/post/stkpushquery/v1/query
        :param data:
        :return response (json):
        """
        expected_keys = [
            'BusinessShortCode', 'Password', 'Timestamp',
            'CheckoutRequestID']
        payload = process_data(expected_keys, data)
        payload["Timestamp"] = generate_timestamp()
        url = urls.get_stk_push_query_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.warning("Mpesa express query request has not been completed")
        return {"message": "Request was not completed"}, 500

    def lipa_na_mpesa_online_payment(self, data):
        """
        Lipa na M-Pesa online payment
        For Lipa Na M-Pesa online payment using STK Push.
        Use this API to initiate online payment on behalf of a customer.
        https://developer.safaricom.co.ke/lipa-na-m-pesa-online/
            apis/post/stkpush/v1/processrequest
        :param data:
        :return response (json):
        """
        expected_keys = [
            "BusinessShortCode", "Password",
            "Amount", "PartyA", "PartyB",
            "PhoneNumber", "CallBackURL",
            "AccountReference", "TransactionDesc"]
        payload = process_data(expected_keys, data)
        payload["Timestamp"] = generate_timestamp()
        payload["TransactionType"] = "CustomerPayBillOnline"
        url = urls.get_stk_push_process_url(self.env)
        req = self.make_request(url, payload, "POST")
        if req:
            return req.json(), req.status_code
        logger.error("Mpesa express request has not been completed")
        return None, 500


def oauth_generate_token(
        consumer_key, consumer_secret, grant_type="client_credentials",
        env="sandbox"):
    """
    Authenticate your app and return an OAuth access token.
    This token gives you time bound access token to call allowed APIs.
    NOTE: The OAuth access token expires after an hour (3600 seconds),
    after which, you will need to generate another access token so you
    need to keep track of this.
    :param consumer_key:
    :param consumer_secret:
    :param grant_type:
    :param env:
    :param version:
    :return response:
    """
    url = urls.get_generate_token_url(env)
    req = requests.get(
        url, params=dict(grant_type=grant_type),
        auth=(consumer_key, consumer_secret))
    if req:
        return req.json(), req.status_code
    logger.warning("Token not generated.")
    return {"message": "Request was not completed"}, 500


def encode_password(shortcode, passkey, timestamp):
    """
    Generate and return a base64 encoded password for online access.
    :param shortcode:
    :param passkey:
    :param timestamp:
    :return base64 encoded password:
    """
    return base64.encode(shortcode + passkey + timestamp)


def generate_timestamp():
    """
    Return the current timestamp formated as YYYYMMDDHHMMSS
    :return current timestamp:
    """
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")


def process_data(expected_keys, data):
    """
    Check for any expected but missing keyword arguments
    and raise a TypeError else return the keywords arguments
    repackaged in a dictionary i.e the payload.
    :param expected_keys:
    :param data:
    :return payload:
    """
    payload = {}
    for key in expected_keys:
        value = data.pop(key, False)
        if not value:
            raise TypeError("Missing value on key {0}".format(key))
        else:
            payload[key] = value
    return payload
