import os

from mpesa_sdk.gateway import oauth_generate_token
from tests.base import BaseTest


class TestGenerateToken(BaseTest):
    def test_generate_token(self):
        result, status_code = oauth_generate_token(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            grant_type="client_credentials",
            env="sandbox")
        assert result is not None
        assert status_code == 200
        assert "access_token" in result
