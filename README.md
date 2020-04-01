**MPESA REST SDK**

[![Language](https://img.shields.io/badge/language-python-green.svg)](https://github.com/sartim/flask_shop_api)
![Build Status](https://github.com/sartim/mpesa-sdk/workflows/Publish%20Python%20Mpesa%20SDK%20distribution%20to%20PyPI/badge.svg)

Simple to use helper sdk for Python developers seeking to integrate MPESA API without much hustle.
Supports Python 2 & 3. 

Urls are found on urls.py and depending on the environment set sandbox or production urls are used.

To generate access token use your client and secret from M-Pesa api account and use oauth_generate_token method.

***Installation***

    $ pip install mpesa-sdk

**Usage**

    from mpesa_sdk.gateway import Mpesa

    access_token = oauth_generate_token(consumer_key="Consumer Key", consumer_secret="Consumer Secret", grant_type="client_credentials", env="sandbox")

    mpesa = Mpesa(access_token)

_C2B Register Url_

    data = {
        "ShortCode": " " ,
        "ResponseType": " ",
        "ConfirmationURL": " ",
        "ValidationURL": " "
    }

    mpesa.c2b_register_url(data)


__C2B Simulate Transaction__
    
    data = {
        "ShortCode": "",
        "CommandID": "CustomerPayBillOnline",
        "Amount": "",
        "Msisdn": "",
        "BillRefNumber": ""
    }
    mpesa.c2b_simulate_transaction(data)
    
__B2B Payment Request__

    data = {
        "Initiator": "",
        "SecurityCredential": "",
        "CommandID": "", 
        "SenderIdentifierType": "",
        "RecieverIdentifierType": "", 
        "Amount": "",
        "PartyA": "",
        "PartyB": "",
        "AccountReference": "",
        "Remarks": "",
        "QueueTimeOutURL": "",
        "ResultURL": ""
    }
    
    mpesa.b2b_payment_request(data)


__B2C Payment Request__

    data = {
        "InitiatorName": "",
        "SecurityCredential": "",
        "CommandID": "",
        "Amount": "",
        "PartyA": "",
        "PartyB": "",
        "Remarks": "",
        "QueueTimeOutURL": "" ,
        "ResultURL": "",
        "Occassion":  ""
    }
    
    mpesa.b2c_payment_request(data)

__Transaction Status__

    data = {
        "Initiator": "",
        "SecurityCredential": "",
        "CommandID": "TransactionStatusQuery",
        "TransactionID": "",
        "PartyA": "",
        "IdentifierType": "1",
        "ResultURL": "",
        "QueueTimeOutURL": "",
        "Remarks": " ",
        "Occasion": " "
    }
    
    mpesa.transation_status_request(data)

__Account Balance__

    data = {
        "Initiator": "",
        "SecurityCredential": "",
        "CommandID": "AccountBalance",
        "PartyA": "",
        "IdentifierType": "4",
        "Remarks": "",
        "QueueTimeOutURL": "",
        "ResultURL": ""
    }
    
    mpesa.account_balance_request(data)

__Reversal Request__

    data = {
        "Initiator": "",
        "SecurityCredential": "",
        "CommandID":"TransactionReversal",
        "TransactionID": "",
        "Amount": "",
        "ReceiverParty": "",
        "RecieverIdentifierType":"11",
        "ResultURL": "",
        "QueueTimeOutURL": "",
        "Remarks": "",
        "Occasion": ""
    }
    
    mpesa.reversal_request(data)
    

    
    
**NOTE**: _Access token generated from M-Pesa API expires after 3599 seconds_