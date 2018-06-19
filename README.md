**MPESA REST API Python SDK**

Helper module for Python developers seeking to integrate MPESA API withput much hustle.
Supports Python2 & 3. 

Urls are found on urls.py and depending on the environment set sandbox or production urls are used.

To generate access token use your client and secret from M-Pesa api account and use oauth_generate_token method.

***Installation***

    $ pip install mpesa-python-sdk

**Usage**

`from mpesa.gateway import Mpesa`

`access_token = oauth_generate_token(consumer_key="Consumer Key", consumer_secret="Consumer Secret", grant_type="client_credentials", env="sandbox")`

`mpesa = Mpesa(access_token)`

`mpesa_lib.c2b_register_url(data)`

**NOTE**: _Access token generated from M-Pesa API expires after 3599 seconds_