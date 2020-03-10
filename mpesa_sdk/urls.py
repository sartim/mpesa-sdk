import os

SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"


def get_base_url(env):
    if env == "sandbox":
        base_url = SANDBOX_BASE_URL
    else:
        base_url = os.environ.get("PROD_URL")
    return base_url


def get_generate_token_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/oauth/v1/generate".format(base_url)


def get_reversal_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/reversal/v1/request".format(base_url)


def get_b2c_payment_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/b2c/v1/paymentrequest".format(base_url)


def get_b2b_payment_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/b2b/v1/paymentrequest".format(base_url)


def get_c2b_register_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/c2b/v1/registerurl".format(base_url)


def get_c2b_simulate_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/c2b/v1/simulate".format(base_url)


def get_transaction_status_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/transactionstatus/v1/query".format(base_url)


def get_account_balance_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/accountbalance/v1/query".format(base_url)


def get_stk_push_query_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/stkpushquery/v1/query".format(base_url)


def get_stk_push_process_url(env="sandbox"):
    base_url = get_base_url(env)
    return "{}/mpesa/stkpush/v1/processrequest".format(base_url)
