"""HTTP client helpers for Safaricom's Daraja APIs."""

from __future__ import annotations

import base64
import math
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from mpesa_sdk import urls

DEFAULT_TIMEOUT = 10.0


class MpesaError(Exception):
    """Base class for Daraja client errors."""


class MpesaConfigurationError(MpesaError, ValueError):
    """Raised when client configuration or a request payload is invalid."""


class MpesaTransportError(MpesaError):
    """Raised when an HTTP request cannot be completed."""


class MpesaRequestError(MpesaError):
    """Raised when Daraja returns a non-success HTTP response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(message)


class MpesaAPIError(MpesaError):
    """Raised when Daraja accepts HTTP but rejects the API request."""

    def __init__(self, code: str | int, message: str):
        self.code = str(code)
        super().__init__(message)


class MpesaResponseError(MpesaError):
    """Raised when Daraja returns an unreadable or invalid response."""


def _required_payload(data: Mapping[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    if not isinstance(data, Mapping):
        raise MpesaConfigurationError("Request data must be a mapping.")

    missing = [key for key in keys if key not in data or data[key] is None or data[key] == ""]
    if missing:
        raise MpesaConfigurationError("Missing required request value(s): " + ", ".join(missing))
    return {key: data[key] for key in keys}


def _validate_timeout(timeout: float) -> float:
    try:
        value = float(timeout)
    except (TypeError, ValueError) as error:
        raise MpesaConfigurationError(
            "timeout must be a positive, finite number of seconds."
        ) from error
    if not math.isfinite(value) or value <= 0:
        raise MpesaConfigurationError("timeout must be a positive, finite number of seconds.")
    return value


def _response_json(response: requests.Response) -> tuple[dict[str, Any], int]:
    try:
        body = response.json()
    except ValueError as error:
        raise MpesaResponseError("Daraja returned a non-JSON response.") from error

    if not isinstance(body, dict):
        raise MpesaResponseError("Daraja returned a JSON response that is not an object.")
    if not response.ok:
        detail = body.get("errorMessage") or body.get("error_description")
        if not detail:
            detail = "Daraja rejected the request."
        raise MpesaRequestError(response.status_code, str(detail))
    response_code = body.get("ResponseCode")
    if response_code not in (None, 0, "0"):
        detail = body.get("ResponseDescription") or body.get("errorMessage")
        raise MpesaAPIError(response_code, str(detail or "Daraja rejected the request."))
    return body, response.status_code


class Mpesa:
    """Small synchronous client for the Daraja REST API.

    ``env`` must be ``sandbox`` or ``production``. ``test`` and ``prod`` are
    accepted as explicit backwards-compatible aliases. Requests have a finite
    timeout unless a positive ``timeout`` is supplied.
    """

    def __init__(
        self,
        access_token: str,
        env: str = "sandbox",
        version: str = "v1",
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if not isinstance(access_token, str) or not access_token.strip():
            raise MpesaConfigurationError("An access token is required.")
        self.timeout = _validate_timeout(timeout)
        try:
            self.env = urls.normalize_environment(env)
        except (TypeError, ValueError) as error:
            raise MpesaConfigurationError(str(error)) from error
        self.headers = {"Authorization": f"Bearer {access_token}"}
        self.version = version

    def make_request(self, url: str, payload: Mapping[str, Any] | None, method: str):
        """Send one request and return its ``requests.Response``.

        This low-level compatibility method raises ``MpesaTransportError`` on
        network failures instead of returning ``None``.
        """
        try:
            return requests.request(
                method,
                url,
                headers=self.headers,
                json=dict(payload) if payload is not None else None,
                timeout=self.timeout,
            )
        except requests.RequestException as error:
            raise MpesaTransportError("The Daraja request could not be completed.") from error

    def _request_json(self, url: str, payload: Mapping[str, Any], method: str = "POST"):
        response = self.make_request(url, payload, method)
        return _response_json(response)

    def b2b_payment_request(self, data: Mapping[str, Any]):
        payload = _required_payload(
            data,
            (
                "Initiator",
                "SecurityCredential",
                "CommandID",
                "SenderIdentifierType",
                "RecieverIdentifierType",
                "Amount",
                "PartyA",
                "PartyB",
                "AccountReference",
                "Remarks",
                "QueueTimeOutURL",
                "ResultURL",
            ),
        )
        return self._request_json(urls.get_b2b_payment_request_url(self.env), payload)

    def b2c_payment_request(self, data: Mapping[str, Any]):
        payload = _required_payload(
            data,
            (
                "InitiatorName",
                "SecurityCredential",
                "CommandID",
                "Amount",
                "PartyA",
                "PartyB",
                "Remarks",
                "QueueTimeOutURL",
                "ResultURL",
                "Occasion",
            ),
        )
        return self._request_json(urls.get_b2c_payment_request_url(self.env), payload)

    def c2b_register_url(self, data: Mapping[str, Any]):
        payload = _required_payload(
            data, ("ShortCode", "ResponseType", "ConfirmationURL", "ValidationURL")
        )
        return self._request_json(urls.get_c2b_register_url(self.env), payload)

    def c2b_simulate_transaction(self, data: Mapping[str, Any]):
        payload = _required_payload(data, ("ShortCode", "Amount", "Msisdn"))
        payload["CommandID"] = "CustomerPayBillOnline"
        return self._request_json(urls.get_c2b_simulate_url(self.env), payload)

    def transaction_status_request(self, data: Mapping[str, Any]):
        """Submit the asynchronous Transaction Status query.

        Safaricom sends the query result later to ``ResultURL``. This method
        returns only the acknowledgement; it does not report the transaction's
        final status.
        """
        required = _required_payload(
            data,
            (
                "Initiator",
                "SecurityCredential",
                "PartyA",
                "ResultURL",
                "QueueTimeOutURL",
                "Remarks",
            ),
        )
        has_transaction_id = data.get("TransactionID") not in (None, "")
        has_original_conversation = data.get("OriginalConversationID") not in (None, "")
        if has_transaction_id == has_original_conversation:
            raise MpesaConfigurationError(
                "Provide exactly one of TransactionID or OriginalConversationID."
            )
        required["CommandID"] = "TransactionStatusQuery"
        required["IdentifierType"] = str(data.get("IdentifierType", "4"))
        if has_transaction_id:
            required["TransactionID"] = data["TransactionID"]
        else:
            required["OriginalConversationID"] = data["OriginalConversationID"]
        if data.get("Occasion") not in (None, ""):
            required["Occasion"] = data["Occasion"]
        return self._request_json(urls.get_transaction_status_url(self.env), required)

    # Preserve the misspelled method shipped in mpesa-sdk 1.0.7.
    def transation_status_request(self, data: Mapping[str, Any]):
        return self.transaction_status_request(data)

    def account_balance_request(self, data: Mapping[str, Any]):
        payload = _required_payload(
            data,
            (
                "Initiator",
                "SecurityCredential",
                "PartyA",
                "Remarks",
                "QueueTimeOutURL",
                "ResultURL",
            ),
        )
        payload["CommandID"] = "AccountBalance"
        payload["IdentifierType"] = str(data.get("IdentifierType", "4"))
        return self._request_json(urls.get_account_balance_url(self.env), payload)

    def reversal_request(self, data: Mapping[str, Any]):
        payload = _required_payload(
            data,
            (
                "Initiator",
                "SecurityCredential",
                "TransactionID",
                "Amount",
                "ReceiverParty",
                "ResultURL",
                "QueueTimeOutURL",
                "Remarks",
                "Occasion",
            ),
        )
        payload["CommandID"] = "TransactionReversal"
        payload["RecieverIdentifierType"] = "4"
        return self._request_json(urls.get_reversal_request_url(self.env), payload)

    def mpesa_express_query(self, data: Mapping[str, Any]):
        """Query an M-Pesa Express/STK Push checkout request."""
        payload = _required_payload(data, ("BusinessShortCode", "Password", "CheckoutRequestID"))
        payload["Timestamp"] = data.get("Timestamp") or generate_timestamp()
        return self._request_json(urls.get_mpesa_express_query_url(self.env), payload)

    def lipa_na_mpesa_online_query(self, data: Mapping[str, Any]):
        """Compatibility alias for :meth:`mpesa_express_query`."""
        return self.mpesa_express_query(data)

    def mpesa_express_payment(self, data: Mapping[str, Any]):
        """Initiate an M-Pesa Express (STK Push) payment prompt."""
        payload = _required_payload(
            data,
            (
                "BusinessShortCode",
                "Password",
                "Amount",
                "PartyA",
                "PartyB",
                "PhoneNumber",
                "CallBackURL",
                "AccountReference",
                "TransactionDesc",
            ),
        )
        payload["Timestamp"] = data.get("Timestamp") or generate_timestamp()
        payload["TransactionType"] = data.get("TransactionType", "CustomerPayBillOnline")
        return self._request_json(urls.get_mpesa_express_payment_url(self.env), payload)

    def lipa_na_mpesa_online_payment(self, data: Mapping[str, Any]):
        """Compatibility alias for :meth:`mpesa_express_payment`."""
        return self.mpesa_express_payment(data)


def oauth_generate_token(
    consumer_key: str,
    consumer_secret: str,
    grant_type: str = "client_credentials",
    env: str = "sandbox",
    timeout: float = DEFAULT_TIMEOUT,
):
    """Return a Daraja OAuth token response and HTTP status code."""
    if not consumer_key or not consumer_secret:
        raise MpesaConfigurationError("Consumer key and consumer secret are required.")
    timeout = _validate_timeout(timeout)
    try:
        url = urls.get_generate_token_url(env)
    except (TypeError, ValueError) as error:
        raise MpesaConfigurationError(str(error)) from error
    try:
        response = requests.get(
            url,
            params={"grant_type": grant_type},
            auth=(consumer_key, consumer_secret),
            timeout=timeout,
        )
    except requests.RequestException as error:
        raise MpesaTransportError("The Daraja token request could not be completed.") from error
    return _response_json(response)


def generate_mpesa_express_password(shortcode: str | int, passkey: str, timestamp: str):
    """Build the Base64 M-Pesa Express password from shortcode, passkey and timestamp."""
    value = f"{shortcode}{passkey}{timestamp}".encode()
    return base64.b64encode(value).decode("ascii")


def encode_password(shortcode: str | int, passkey: str, timestamp: str):
    """Compatibility alias for :func:`generate_mpesa_express_password`."""
    return generate_mpesa_express_password(shortcode, passkey, timestamp)


def generate_timestamp(now: datetime | None = None):
    """Return the Daraja timestamp in East Africa Time as ``YYYYMMDDHHMMSS``."""
    eat = timezone(timedelta(hours=3), name="EAT")
    current = now or datetime.now(eat)
    if current.tzinfo is not None:
        current = current.astimezone(eat)
    return current.strftime("%Y%m%d%H%M%S")


def process_data(expected_keys, data):
    """Compatibility validator that copies data and preserves valid zero values."""
    return _required_payload(data, tuple(expected_keys))
