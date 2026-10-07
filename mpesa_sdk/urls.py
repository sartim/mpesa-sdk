SANDBOX_BASE_URL = "https://sandbox.safaricom.co.ke"
PROD_BASE_URL = "https://api.safaricom.co.ke"


def normalize_environment(env):
    """Normalize supported names and reject unknown values instead of using production."""
    if not isinstance(env, str):
        raise TypeError("env must be 'sandbox' or 'production'.")
    normalized = env.strip().lower()
    aliases = {
        "sandbox": "sandbox",
        "test": "sandbox",
        "production": "production",
        "prod": "production",
    }
    try:
        return aliases[normalized]
    except KeyError as error:
        raise ValueError("env must be 'sandbox' or 'production'.") from error


def get_base_url(env):
    return {
        "sandbox": SANDBOX_BASE_URL,
        "production": PROD_BASE_URL,
    }[normalize_environment(env)]


def get_generate_token_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/oauth/v1/generate"


def get_reversal_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/reversal/v1/request"


def get_b2c_payment_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/b2c/v1/paymentrequest"


def get_b2b_payment_request_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/b2b/v1/paymentrequest"


def get_c2b_register_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/c2b/v1/registerurl"


def get_c2b_simulate_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/c2b/v1/simulate"


def get_transaction_status_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/transactionstatus/v1/query"


def get_account_balance_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/accountbalance/v1/query"


def get_stk_push_query_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/stkpushquery/v1/query"


def get_stk_push_process_url(env="sandbox"):
    base_url = get_base_url(env)
    return f"{base_url}/mpesa/stkpush/v1/processrequest"


def get_mpesa_express_query_url(env="sandbox"):
    """Current Daraja name for the legacy STK Push query endpoint."""
    return get_stk_push_query_url(env)


def get_mpesa_express_payment_url(env="sandbox"):
    """Current Daraja name for the legacy STK Push payment endpoint."""
    return get_stk_push_process_url(env)
