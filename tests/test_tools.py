import sys
import os
sys.path.append(os.path.abspath('../app'))
from app import tools


def test_create_account_change_response():
    first_acc = {
        "account": "test_account",
        "repositories_number": "10",
        "followers": "100",
        "following": "50",
        "contributions_last_year": "150"
    }
    last_acc = {
        "account": "test_account",
        "repositories_number": "15",
        "followers": "120",
        "following": "55",
        "contributions_last_year": "180"
    }
    response = tools.create_account_change_response(first_acc, last_acc)
    assert response["account"] == "test_account"
    assert response["repositories_number"] == "15 (+5)"
    assert response["followers"] == "120 (+20)"
    assert response["following"] == "55 (+5)"
    assert response["contributions_last_year"] == "180 (+30)"

def test_create_repository_change_response():
    first_repo = {
        "account": "test_account",
        "repository": "test_repo",
        "branches": "5",
        "tags": "10",
        "commits": "50",
        "stars": "100",
        "watching": "20",
        "forks": "30"
    }
    last_repo = {
        "account": "test_account",
        "repository": "test_repo",
        "branches": "7",
        "tags": "12",
        "commits": "55",
        "stars": "105",
        "watching": "25",
        "forks": "35"
    }
    response = tools.create_repository_change_response(first_repo, last_repo)
    assert response["account"] == "test_account"
    assert response["repository"] == "test_repo"
    assert response["branches"] == "7 (+2)"
    assert response["tags"] == "12 (+2)"
    assert response["commits"] == "55 (+5)"
    assert response["stars"] == "105 (+5)"
    assert response["watching"] == "25 (+5)"
    assert response["forks"] == "35 (+5)"
