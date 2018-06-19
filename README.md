**MPESA REST API Python SDK**

Helper module for Python developers seeking to integrate MPESA API withput much hustle.
Supports Python2 & 3. 

Urls are found on urls.py and depending on the environment set sandbox or production urls are used.

To generate access token use your client and secret from mpesa api account and use oauth_generate_token method.

***Setup***

* Export environment variables
***
For sandbox

    $ export ENV="sandbox"
For production

    $ export ENV="production"
