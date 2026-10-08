# M-Pesa SDK

[![CI](https://github.com/sartim/mpesa-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/sartim/mpesa-sdk/actions/workflows/ci.yml)

`mpesa-sdk` is a synchronous Python client for Safaricom Daraja REST APIs. The
distribution name used by pip is `mpesa-sdk`; its Python import package is
`mpesa_sdk`.

## Install

```shell
python -m pip install mpesa-sdk
```

For local development and tests:

```shell
python -m pip install 'mpesa-sdk[test]'
```

## Supported API names

The client uses current Daraja API terminology for M-Pesa Express and
Transaction Status:

| Daraja capability | SDK method |
| --- | --- |
| M-Pesa Express (STK Push) | `Mpesa.mpesa_express_payment(data)` |
| M-Pesa Express query | `Mpesa.mpesa_express_query(data)` |
| Transaction Status query | `Mpesa.transaction_status_request(data)` |
| OAuth token | `oauth_generate_token(...)` |

Compatibility methods remain available for existing users:

- `lipa_na_mpesa_online_payment` aliases `mpesa_express_payment`.
- `lipa_na_mpesa_online_query` aliases `mpesa_express_query`.
- The historical typo `transation_status_request` aliases
  `transaction_status_request`.

Successful requests return `(response_json, http_status_code)`. Network
failures, non-2xx responses, invalid JSON, and Daraja API rejections raise the
documented `MpesaError` subclasses. Requests use a 10 second timeout by
default; a different positive timeout can be supplied to `Mpesa` or the OAuth
helper.

## Configure a sandbox client

Keep the consumer key, consumer secret, passkey, and shortcode in a secret
manager or environment variables. Do not put real credentials in source code,
logs, or a client application.

```python
import os

from mpesa_sdk import Mpesa, oauth_generate_token

token_response, _ = oauth_generate_token(
    os.environ["DARAJA_CONSUMER_KEY"],
    os.environ["DARAJA_CONSUMER_SECRET"],
    env="sandbox",
)
client = Mpesa(token_response["access_token"], env="sandbox")
```

The environment must be `sandbox` or `production`. For compatibility, `test`
is an alias for `sandbox`, and `prod` is an alias for `production`. Unknown
values raise `MpesaConfigurationError`; they never select production by
default.

## M-Pesa Express (STK Push)

The SDK sends the request; the integrating application creates the request
data and handles asynchronous callbacks.

```python
from mpesa_sdk import generate_mpesa_express_password, generate_timestamp

timestamp = generate_timestamp()
payload = {
    "BusinessShortCode": shortcode,
    "Password": generate_mpesa_express_password(shortcode, passkey, timestamp),
    "Timestamp": timestamp,
    "Amount": 10,
    "PartyA": "254700000000",
    "PartyB": shortcode,
    "PhoneNumber": "254700000000",
    "CallBackURL": "https://example.invalid/daraja/stk/callback",
    "AccountReference": "INV-1001",
    "TransactionDesc": "Invoice payment",
}
response, status_code = client.mpesa_express_payment(payload)
```

`generate_timestamp()` returns the Daraja timestamp in East Africa Time.
`generate_mpesa_express_password()` Base64-encodes the shortcode, passkey, and
timestamp combination used by M-Pesa Express. The former `encode_password()`
name remains available as a compatibility alias.

## Transaction Status

Transaction Status is asynchronous. The immediate response acknowledges query
submission; the eventual transaction result is delivered separately to the
configured `ResultURL`. Provide exactly one of `TransactionID` (M-Pesa receipt)
or `OriginalConversationID`.

```python
acknowledgement, status_code = client.transaction_status_request(
    {
        "Initiator": os.environ["DARAJA_INITIATOR"],
        "SecurityCredential": os.environ["DARAJA_SECURITY_CREDENTIAL"],
        "TransactionID": "RECEIPT123",
        "PartyA": shortcode,
        "IdentifierType": "4",
        "ResultURL": "https://example.invalid/daraja/status/result",
        "QueueTimeOutURL": "https://example.invalid/daraja/status/timeout",
        "Remarks": "Reconcile invoice payment",
    }
)
```

The default `IdentifierType` is `4`, the organization shortcode type used by
the Daraja Transaction Status API. Set it explicitly if the transaction
requires a different party type.

## Errors

- `MpesaConfigurationError`: invalid client configuration or missing request
  values.
- `MpesaTransportError`: connection or timeout failure.
- `MpesaRequestError`: non-success HTTP response; `status_code` is available.
- `MpesaAPIError`: Daraja returned an API-level rejection; `code` is available.
- `MpesaResponseError`: the response was not a JSON object.

The SDK does not validate callback authenticity, correlate callbacks with
business records, or decide whether to create a ledger payment. Applications
must validate and deduplicate callbacks, correlate them with the original
attempt, and use an authoritative reconciliation result before recording
payments. Never treat an accepted request or customer prompt as proof that
funds were received.

## Development

The test suite mocks HTTP and never contacts Safaricom or requires credentials.

```shell
python -m pip install -e '.[test]'
python -m pytest
ruff check .
ruff format --check .
```

### Releases

Merging changes to `master` runs CI first. If CI passes, Python Semantic
Release reads Conventional Commit messages to decide whether to make a release,
updates the project version and changelog, creates a GitHub release, and
publishes the package to PyPI. Use `feat:` for new features, `fix:` for bug
fixes, and `!` or a `BREAKING CHANGE:` footer for breaking changes. Prefix
non-release changes with types such as `docs:`, `chore:`, or `test:`.

## License

MIT
