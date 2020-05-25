**MPESA REST SDK**

[![Language](https://img.shields.io/badge/language-python-green.svg)](https://github.com/sartim/mpesa-sdk)
![Build Status](https://github.com/sartim/mpesa-sdk/workflows/Publish%20Python%20Mpesa%20SDK%20distribution%20to%20PyPI/badge.svg)

Pure python sdk for [MPESA API](https://developer.safaricom.co.ke/docs#authentication).


**Features**

* Generate Token
* C2B Register Url
* C2B Simulate Transaction
* C2B Simulate Transaction
* B2B Payment Request
* B2C Payment Request
* Transaction Status
* Account Balance
* Reversal Request

***Installation***

    $ pip install mpesa-sdk

***Running tests***

Create .env file from [example](https://github.com/sartim/mpesa-sdk/blob/master/.env.example) then run
    
    $ pip install pytest
    $ pytest
 
To test for different python environments use
    
    $ pip install tox
    $ tox
 
Read more on [wiki](https://github.com/sartim/mpesa-sdk/wiki).
