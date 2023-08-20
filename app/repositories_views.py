import datetime
import time
import requests

from flask import request, abort
from .app import app
from .tools import create_repository_change_response
from .models import repositories_data
from .parsing.repos_parsing import RepositoryParse


@app.route("/repos/add", methods=['POST'])
def add_new_repository():
    request_data = request.get_json()
    if len(request_data) != 2 or not 'account' in request_data or not 'repository' in request_data:
        abort(400)
    account = request_data["account"]
    repository = request_data["repository"]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    response = requests.get(f'http://github.com/{account}/{repository}')
    if response.status_code != 200:
        abort(response.status_code)

    confirmed_account = RepositoryParse(account, repository)
    new_document = {
        "account": account,
        "repository": repository,
        "branches": confirmed_account.get_branches(),
        "tags": confirmed_account.get_tags(),
        "commits": confirmed_account.get_commits(),
        "stars": confirmed_account.get_stars(),
        "watching": confirmed_account.get_watching(),
        "forks": confirmed_account.get_forks(),
        "time": time_now
    }
    repositories_data.insert_one(new_document)
    added_document = repositories_data.find_one({"time": time_now, "account": account, "repository": repository})
    response = {
        "account": added_document["account"],
        "repository": added_document["repository"],
        "branches": added_document["branches"],
        "tags": added_document["tags"],
        "commits": added_document["commits"],
        "stars": added_document["stars"],
        "watching": added_document["watching"],
        "forks": added_document["forks"],
        "time": added_document["time"]
    }
    return (response, 201)

@app.route("/repos/stats", methods=['GET'])
def get_repos_stat():
    account = request.args.get('account')
    repository = request.args.get('repository')
    time_from = request.args.get('from')
    time_to = request.args.get('to')

    if not time_from or not time_to or not account or not repository:
        abort(400)
    response = requests.get(f'http://github.com/{account}/{repository}')
    if response.status_code != 200:
        abort(response.status_code)
    try:
        valid_time_from = time.strptime(time_from, "%d-%m-%Y %H:%M")
        valid_time_to = time.strptime(time_to, "%d-%m-%Y %H:%M")
    except ValueError:
        abort(415)

    chosen_repos = {}
    counter = 0
    for document in repositories_data.find({
        "account": account, "repository": repository, "time": {"$lte": time_to, "$gte": time_from}
    }).sort("time"):
        chosen_repos[counter] = {
            "account": document["account"],
            "repository": document["repository"],
            "branches": document["branches"],
            "tags": document["tags"],
            "commits": document["commits"],
            "stars": document["stars"],
            "watching": document["watching"],
            "forks": document["forks"],
            "time": document["time"]
        }
        counter += 1
    if counter == 0:
        return ({"get_stat": "no_changes_in_this_interval"}, 200)
    return (create_repository_change_response(chosen_repos[0], chosen_repos[counter-1]), 200)

@app.route("/repos/delete/all", methods=['DELETE'])
def delete_all_repos():
    repositories_data.drop()
    return ({"delete_all_repositories": "OK"}, 200)

@app.route("/repos/delete", methods=['DELETE'])
def delete_repository():
    request_data = request.get_json()
    if len(request_data) != 2 or not 'account' in request_data or not 'repository' in request_data:
        abort(400)

    search_for_repository = repositories_data.find_one({"account": request_data['account'], "repository": request_data['repository']})
    if not search_for_repository:
        abort(404)
    repositories_data.delete_many({"account": request_data['account'], "repository": request_data['repository']})
    return ({"delete_repository": "OK"}, 200)