"""Manually verify OAuth credentials against the Daraja sandbox."""

import os
import sys

from mpesa_sdk import MpesaError, oauth_generate_token


def main() -> int:
    consumer_key = os.environ.get("DARAJA_SANDBOX_CONSUMER_KEY")
    consumer_secret = os.environ.get("DARAJA_SANDBOX_CONSUMER_SECRET")
    if not consumer_key or not consumer_secret:
        print("Required sandbox OAuth secrets are not configured.", file=sys.stderr)
        return 1

    try:
        token_response, status_code = oauth_generate_token(
            consumer_key,
            consumer_secret,
            env="sandbox",
        )
    except MpesaError as error:
        print(f"Sandbox OAuth request failed ({type(error).__name__}).", file=sys.stderr)
        return 1

    if status_code != 200 or not token_response.get("access_token"):
        print("Sandbox OAuth response did not contain a usable token.", file=sys.stderr)
        return 1

    print("Sandbox OAuth check succeeded. Access token was not displayed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
