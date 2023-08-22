import os
import sys
import requests
import datetime
import mongomock
import pytest
from unittest.mock import Mock, MagicMock, patch

sys.path.append(os.path.abspath('../app'))
from app.app import app
from app.parsing.repos_parsing import RepositoryParse


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_db():
    temp_db = mongomock.MongoClient().db
    yield temp_db

class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

######################################################################################
#                            ''' check /repos/add  '''
######################################################################################

def test_add_new_repository_success(client, monkeypatch):
    mock_repository_parse = Mock(spec=RepositoryParse)
    monkeypatch.setattr('app.parsing.repos_parsing.RepositoryParse', mock_repository_parse)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = 'Mock response text'

    monkeypatch.setattr('requests.get', Mock(return_value=mock_response))
    data = {
        "account": "YaArtem333",
        "repository": "github-tracking-tool"
    }
    response = client.post('/repos/add', json=data)
    assert response.status_code == 201
    assert response.json["account"] == "YaArtem333"
    assert response.json["repository"] == "github-tracking-tool"
    assert response.json["time"] == datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

def test_add_new_repository_bad_request(client):
    response = client.post('/repos/add', json={})
    assert response.status_code == 400

def test_add_new_account_github_error(client, monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(404)

    monkeypatch.setattr(requests, 'get', mock_get)
    data = {"account": "nonexistent_account", "repository": "nonexistent_repository"}
    response = client.post('/repos/add', json=data)
    assert response.status_code == 404

######################################################################################
#                            ''' check /repos/stats  '''
######################################################################################

def test_get_repos_stats_success(client, monkeypatch):
    # Моки для requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    monkeypatch.setattr('requests.get', Mock(return_value=mock_response))
    # Моки для accounts_data.find
    mock_find = MagicMock()
    mock_find.sort.return_value = [
        {
            "account": "test_account",
            "repository": "test_repository",
            "branches": 0,
            "tags": 0,
            "commits": 0,
            "stars": 0,
            "watching": 0,
            "forks": 0,
            "time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        }
    ]
    monkeypatch.setattr('app.models.repositories_data.find', mock_find)
    response = client.get('/repos/stats?account=test_account&repository=test_repository&from=01-01-2023 00:00&to=31-12-2023 23:59')
    assert response.status_code == 200

def test_get_repos_stat_missing_parameters(client):
    response = client.get('/repos/stats')
    assert response.status_code == 400

def test_get_repos_stat_invalid_time_format(client):
    response = client.get('/accounts/stats?account=YaArtem333&from=2023-01-01 00:00&to=2023-12-31 23:59')
    assert response.status_code == 415

def test_get_repos_stat_account_not_found(client, monkeypatch):
    # Мок для requests.get
    mock_response = Mock()
    mock_response.status_code = 404
    monkeypatch.setattr('requests.get', Mock(return_value=mock_response))
    response = client.get('/repos/stats?account=nonexistent_account&repository=nonexistent_repository&from=01-01-2023 00:00&to=31-12-2023 23:59')
    assert response.status_code == 404

def test_get_repos_stat_no_changes_in_interval(client, monkeypatch):
    # Моки для requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    monkeypatch.setattr('requests.get', Mock(return_value=mock_response))
    # Моки для accounts_data.find
    mock_find = MagicMock()
    mock_find.sort.return_value = []
    monkeypatch.setattr('app.models.accounts_data.find', mock_find)
    response = client.get('/accounts/stats?account=test_account&repository=test_repository&from=01-01-2023 00:00&to=31-12-2023 23:59')
    assert response.status_code == 200
    assert response.json == {
        "get_stat": "no_changes_in_this_interval"
    }

######################################################################################
#                            ''' check /accounts/delete/all  '''
######################################################################################

def test_delete_all_repos_success(temp_db, client):
    with patch('app.models.repositories_data', temp_db):
        # Добавляем репозиторий
        response_add = client.post('/repos/add', json={"account": "YaArtem333", "repository": "github-tracking-tool"})
        assert response_add.status_code == 201
        # Удаляем все репозитории аккаунта
        response_delete = client.delete('/repos/delete/all')
        assert response_delete.status_code == 200
        assert response_delete.json == {"delete_all_repositories": "OK"}
        # Проверяем, что репозитории были удалены
        assert temp_db.repositories_data.count_documents({}) == 0

######################################################################################
#                            ''' check /accounts/delete  '''
######################################################################################

def test_add_and_delete_repository(temp_db, client):
    with patch('app.models.repositories_data', temp_db):
        # Добавляем репозиторий
        response_add = client.post('/repos/add', json={"account": "YaArtem333", "repository": "github-tracking-tool"})
        assert response_add.status_code == 201
        # Удаляем репозиторий
        response_delete = client.delete('/repos/delete', json={"account": "YaArtem333", "repository": "github-tracking-tool"})
        assert response_delete.status_code == 200
        assert response_delete.json == {"delete_repository": "OK"}
        # Проверяем, что репозиторий был действительно удален
        assert temp_db.repositories_data.find_one({"account": "YaArtem333", "repository": "github-tracking-tool"}) is None

def test_delete_repository_invalid_request(temp_db, client):
    with patch('app.models.repositories_data'):
        response = client.delete('/repos/delete', json={})
        assert response.status_code == 400

def test_delete_account_not_found(temp_db, client):
    with patch('app.models.repositories_data'):
        response = client.delete('/repos/delete', json={"account": "nonexistent_account", "repository": "nonexistent_repository"})
        assert response.status_code == 404