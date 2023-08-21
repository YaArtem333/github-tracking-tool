import datetime
import os
import sys
import json

sys.path.append(os.path.abspath('../app'))
from app.app import app


class TestGetAccountsData:

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_valid_request(self):
        response = self.client.get("/accounts/stats?account=YaArtem333&from=08-08-2023 17:20&to=21-08-2023 19:35")
        assert response.status_code == 200
        assert response.json["account"] == "YaArtem333"
        assert str(response.json["repositories_number"])
        assert str(response.json["followers"])
        assert str(response.json["following"])
        assert str(response.json["contributions_last_year"])

    def finish_tests(self):
        pass