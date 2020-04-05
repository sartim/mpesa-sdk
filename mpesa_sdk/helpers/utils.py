import logging
import base64
import time


def encode_string(txt):
    """Base64 Encode String"""
    try:
        encoded_string = base64.b64encode(txt.encode())
    except Exception as e:
        logging.error(str(e))
    else:
        return encoded_string
    return False


def current_timestamp(ms=True):
    """Retrieves up to milliseconds when set to true.
    Otherwise return to second
    """
    to_second = time.time()
    if ms:
        return int((to_second + 0.5) * 1000)
    return to_second


def convert_datetime_to_int(dt_time):
    """Convert date time object to integer"""
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day + dt_time.second
