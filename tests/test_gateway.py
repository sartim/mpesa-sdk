import json
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import requests

from mpesa_sdk import (
    Mpesa,
    MpesaAPIError,
    MpesaConfigurationError,
    MpesaRequestError,
    MpesaResponseError,
    MpesaTransportError,
    encode_password,
    generate_mpesa_express_password,
    generate_timestamp,
    oauth_generate_token,
    urls,
)


def make_response(body, status_code=200):
    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(body).encode("utf-8")
    response.encoding = "utf-8"
    return response


def test_install_and_import_names_are_stable():
    import mpesa_sdk

    assert mpesa_sdk.__version__ == "1.1.0"
    assert Mpesa is mpesa_sdk.Mpesa


@pytest.mark.parametrize(
    ("env", "base_url"),
    [
        ("sandbox", urls.SANDBOX_BASE_URL),
        ("test", urls.SANDBOX_BASE_URL),
        ("production", urls.PROD_BASE_URL),
        ("prod", urls.PROD_BASE_URL),
    ],
)
def test_known_environment_names(env, base_url):
    assert urls.get_base_url(env) == base_url


def test_unknown_environment_never_falls_back_to_production():
    with pytest.raises(MpesaConfigurationError):
        Mpesa("token", env="prodcution")
    with pytest.raises(ValueError):
        urls.get_base_url("prodcution")


@pytest.mark.parametrize("timeout", [None, 0, -1, float("inf"), float("nan"), "bad"])
def test_timeout_must_be_finite_and_positive(timeout):
    with pytest.raises(MpesaConfigurationError):
        Mpesa("token", timeout=timeout)


def test_oauth_request_uses_sandbox_and_finite_timeout(monkeypatch):
    response = make_response({"access_token": "token", "expires_in": "3599"})
    get = Mock(return_value=response)
    monkeypatch.setattr(requests, "get", get)

    body, status = oauth_generate_token("key", "secret", env="sandbox")

    assert body["access_token"] == "token"
    assert status == 200
    assert get.call_args.kwargs["timeout"] == 10.0
    assert get.call_args.args[0] == "https://sandbox.safaricom.co.ke/oauth/v1/generate"
    assert get.call_args.kwargs["auth"] == ("key", "secret")


def test_oauth_rejects_unknown_environment_and_reports_transport_error(monkeypatch):
    with pytest.raises(MpesaConfigurationError):
        oauth_generate_token("key", "secret", env="sand-box")

    get = Mock(side_effect=requests.Timeout())
    monkeypatch.setattr(requests, "get", get)
    with pytest.raises(MpesaTransportError):
        oauth_generate_token("key", "secret")


def test_mpesa_express_request_uses_current_api_name_and_does_not_mutate_input(monkeypatch):
    data = {
        "BusinessShortCode": "174379",
        "Password": "encoded",
        "Timestamp": "20260102112233",
        "Amount": 25,
        "PartyA": "254700000000",
        "PartyB": "174379",
        "PhoneNumber": "254700000000",
        "CallBackURL": "https://example.invalid/stk/callback",
        "AccountReference": "INV-1001",
        "TransactionDesc": "Invoice payment",
    }
    original = data.copy()
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token", env="sandbox")

    body, status = client.mpesa_express_payment(data)

    assert body["ResponseCode"] == "0"
    assert status == 200
    assert data == original
    assert request.call_args.args[:2] == (
        "POST",
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
    )
    assert request.call_args.kwargs["json"] == {
        **original,
        "TransactionType": "CustomerPayBillOnline",
    }
    assert request.call_args.kwargs["timeout"] == 10.0


def test_mpesa_express_legacy_alias_remains_available(monkeypatch):
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token")
    data = {
        "BusinessShortCode": "174379",
        "Password": "encoded",
        "Amount": 1,
        "PartyA": "254700000000",
        "PartyB": "174379",
        "PhoneNumber": "254700000000",
        "CallBackURL": "https://example.invalid/callback",
        "AccountReference": "INV-1",
        "TransactionDesc": "Test",
    }

    client.lipa_na_mpesa_online_payment(data)

    assert request.call_args.kwargs["json"]["TransactionType"] == "CustomerPayBillOnline"


def test_transaction_status_supports_receipt_or_original_conversation(monkeypatch):
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token", env="sandbox")
    base = {
        "Initiator": "api-user",
        "SecurityCredential": "encrypted",
        "PartyA": "600000",
        "ResultURL": "https://example.invalid/status/result",
        "QueueTimeOutURL": "https://example.invalid/status/timeout",
        "Remarks": "Reconcile invoice",
    }

    client.transaction_status_request({**base, "TransactionID": "ABC123"})
    receipt_payload = request.call_args.kwargs["json"]
    assert receipt_payload["TransactionID"] == "ABC123"
    assert receipt_payload["IdentifierType"] == "4"
    assert receipt_payload["CommandID"] == "TransactionStatusQuery"
    assert "OriginalConversationID" not in receipt_payload

    client.transaction_status_request(
        {**base, "OriginalConversationID": "origin-123", "Occasion": "INV-1"}
    )
    conversation_payload = request.call_args.kwargs["json"]
    assert conversation_payload["OriginalConversationID"] == "origin-123"
    assert conversation_payload["Occasion"] == "INV-1"
    assert "TransactionID" not in conversation_payload

    with pytest.raises(MpesaConfigurationError):
        client.transaction_status_request(base)
    with pytest.raises(MpesaConfigurationError):
        client.transaction_status_request(
            {**base, "TransactionID": "ABC123", "OriginalConversationID": "origin-123"}
        )


def test_legacy_transaction_status_typo_remains_available(monkeypatch):
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token")
    client.transation_status_request(
        {
            "Initiator": "api-user",
            "SecurityCredential": "encrypted",
            "TransactionID": "ABC123",
            "PartyA": "600000",
            "ResultURL": "https://example.invalid/result",
            "QueueTimeOutURL": "https://example.invalid/timeout",
            "Remarks": "Check",
        }
    )
    assert request.call_args.kwargs["json"]["IdentifierType"] == "4"


def test_stk_query_is_distinct_from_transaction_status(monkeypatch):
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token")

    client.mpesa_express_query(
        {
            "BusinessShortCode": "174379",
            "Password": "encoded",
            "Timestamp": "20260102112233",
            "CheckoutRequestID": "ws_CO_123",
        }
    )

    assert request.call_args.args[1].endswith("/mpesa/stkpushquery/v1/query")


def test_daraja_api_rejections_raise_an_explicit_error(monkeypatch):
    request = Mock(
        return_value=make_response({"ResponseCode": "1", "ResponseDescription": "Request rejected"})
    )
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token")

    with pytest.raises(MpesaAPIError, match="Request rejected") as error:
        client.mpesa_express_query(
            {
                "BusinessShortCode": "174379",
                "Password": "encoded",
                "CheckoutRequestID": "ws_CO_123",
            }
        )
    assert error.value.code == "1"


def test_http_transport_and_malformed_response_errors(monkeypatch):
    client = Mpesa("token")
    monkeypatch.setattr(
        requests,
        "request",
        Mock(return_value=make_response({"errorMessage": "Not authorized"}, 401)),
    )
    with pytest.raises(MpesaRequestError) as error:
        client.mpesa_express_query(
            {
                "BusinessShortCode": "174379",
                "Password": "encoded",
                "CheckoutRequestID": "ws_CO_123",
            }
        )
    assert error.value.status_code == 401

    malformed = requests.Response()
    malformed.status_code = 200
    malformed._content = b"not-json"
    monkeypatch.setattr(requests, "request", Mock(return_value=malformed))
    with pytest.raises(MpesaResponseError):
        client.mpesa_express_query(
            {
                "BusinessShortCode": "174379",
                "Password": "encoded",
                "CheckoutRequestID": "ws_CO_123",
            }
        )

    monkeypatch.setattr(requests, "request", Mock(side_effect=requests.Timeout()))
    with pytest.raises(MpesaTransportError):
        client.mpesa_express_query(
            {
                "BusinessShortCode": "174379",
                "Password": "encoded",
                "CheckoutRequestID": "ws_CO_123",
            }
        )


def test_encode_password_and_timestamp_use_eat():
    expected = "MTc0Mzc5cGFzc2tleTIwMjYwMTAyMTEyMjMz"
    assert generate_mpesa_express_password("174379", "passkey", "20260102112233") == expected
    assert encode_password("174379", "passkey", "20260102112233") == expected
    utc = datetime(2026, 1, 2, 8, 22, 33, tzinfo=timezone.utc)
    assert generate_timestamp(utc) == "20260102112233"


def test_process_data_does_not_mutate_and_accepts_zero():
    from mpesa_sdk.gateway import process_data

    data = {"Amount": 0, "Reference": "INV-0"}
    original = data.copy()
    assert process_data(("Amount", "Reference"), data) == original
    assert data == original


@pytest.mark.parametrize(
    ("method_name", "data", "endpoint", "added_fields"),
    [
        (
            "b2b_payment_request",
            {
                "Initiator": "api-user",
                "SecurityCredential": "encrypted",
                "CommandID": "BusinessPayBill",
                "SenderIdentifierType": "4",
                "RecieverIdentifierType": "4",
                "Amount": 10,
                "PartyA": "600000",
                "PartyB": "600001",
                "AccountReference": "INV-1",
                "Remarks": "Supplier payment",
                "QueueTimeOutURL": "https://example.invalid/timeout",
                "ResultURL": "https://example.invalid/result",
            },
            "/mpesa/b2b/v1/paymentrequest",
            {},
        ),
        (
            "b2c_payment_request",
            {
                "InitiatorName": "api-user",
                "SecurityCredential": "encrypted",
                "CommandID": "SalaryPayment",
                "Amount": 10,
                "PartyA": "600000",
                "PartyB": "254700000000",
                "Remarks": "Salary",
                "QueueTimeOutURL": "https://example.invalid/timeout",
                "ResultURL": "https://example.invalid/result",
                "Occasion": "Payroll",
            },
            "/mpesa/b2c/v1/paymentrequest",
            {},
        ),
        (
            "c2b_register_url",
            {
                "ShortCode": "600000",
                "ResponseType": "Completed",
                "ConfirmationURL": "https://example.invalid/confirm",
                "ValidationURL": "https://example.invalid/validate",
            },
            "/mpesa/c2b/v1/registerurl",
            {},
        ),
        (
            "c2b_simulate_transaction",
            {"ShortCode": "600000", "Amount": 10, "Msisdn": "254700000000"},
            "/mpesa/c2b/v1/simulate",
            {"CommandID": "CustomerPayBillOnline"},
        ),
        (
            "account_balance_request",
            {
                "Initiator": "api-user",
                "SecurityCredential": "encrypted",
                "PartyA": "600000",
                "Remarks": "Reconcile account",
                "QueueTimeOutURL": "https://example.invalid/timeout",
                "ResultURL": "https://example.invalid/result",
            },
            "/mpesa/accountbalance/v1/query",
            {"CommandID": "AccountBalance", "IdentifierType": "4"},
        ),
        (
            "reversal_request",
            {
                "Initiator": "api-user",
                "SecurityCredential": "encrypted",
                "TransactionID": "ABC123",
                "Amount": 10,
                "ReceiverParty": "600000",
                "ResultURL": "https://example.invalid/result",
                "QueueTimeOutURL": "https://example.invalid/timeout",
                "Remarks": "Reverse duplicate payment",
                "Occasion": "INV-1",
            },
            "/mpesa/reversal/v1/request",
            {"CommandID": "TransactionReversal", "RecieverIdentifierType": "4"},
        ),
    ],
)
def test_additional_endpoint_wrappers_send_payload_without_mutating_input(
    monkeypatch, method_name, data, endpoint, added_fields
):
    request = Mock(return_value=make_response({"ResponseCode": "0"}))
    monkeypatch.setattr(requests, "request", request)
    client = Mpesa("token", env="sandbox")
    original = data.copy()

    body, status = getattr(client, method_name)(data)

    assert body["ResponseCode"] == "0"
    assert status == 200
    assert data == original
    assert request.call_args.args == ("POST", f"https://sandbox.safaricom.co.ke{endpoint}")
    assert request.call_args.kwargs["json"] == {**original, **added_fields}
    assert request.call_args.kwargs["headers"] == {"Authorization": "Bearer token"}
    assert request.call_args.kwargs["timeout"] == 10.0
