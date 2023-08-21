import datetime
import os
import sys
import json

sys.path.append(os.path.abspath('../app'))
from app.app import app


class TestAddAccountData:

    def setup(self):
        app.testing = True
        self.client = app.test_client()

    def test_valid_request(self):
        response = self.client.post("/accounts/add", json={"account": "YaArtem333"})
        assert response.status_code == 201
        assert response.json["account"] == "YaArtem333"
        assert int(response.json["repositories_number"])
        assert list(response.json["popular_repositories"])
        #assert int(response.json["followers"])
        assert int(response.json["following"])
        assert int(response.json["contributions_last_year"])
        assert response.json["time"] == datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    def test_invalid_request_no_account_in_request_400(self):
        response = self.client.post("/accounts/add", json={"": "YaArtem333"})
        assert response.status_code == 400
        assert response.json["error"] == "bad request"

    def test_invalid_request_extra_data_in_request_400(self):
        response = self.client.post("/accounts/add", json={"account": "YaArtem333", "qwerty": "123456"})
        assert response.status_code == 400
        assert response.json["error"] == "bad request"

    def test_invalid_request_no_value_in_request_400(self):
        response = self.client.post("/accounts/add", json={"account": ""})
        assert response.status_code == 400
        assert response.json["error"] == "bad request"

    def test_invalid_request_wrong_data_type_415(self):
        response = self.client.post("/accounts/add", data={"account": "YaArtem333"})
        assert response.status_code == 415
        assert response.json["error"] == "unsupported media type"

    def finish_tests(self):
        pass
