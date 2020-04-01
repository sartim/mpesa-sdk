import logging
import base64


def encode_string(txt):
    """Base64 Encode String"""
    try:
        encoded_string = base64.b64encode(txt.encode())
    except Exception as e:
        logging.error(str(e))
    else:
        return encoded_string
    return False
