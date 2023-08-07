import datetime
import time

from flask import request, abort
from .app import app
from .models import repositories_data


@app.route("/repos/add", methods=['POST'])
def add_new_repository():
    request_data = request.get_json()
    if len(request_data) != 2:
        abort(400)
    account = request_data["account"]
    repository = request_data["repository"]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    new_document = {"account": account, "repository": repository, "time": time_now}
    repositories_data.insert_one(new_document)

    added_document = repositories_data.find_one({"time": time_now, "account": account, "repository": repository})
    response = {
        "account": added_document["account"],
        "repository": added_document["repository"],
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
    try:
        valid_time_from = time.strptime(time_from, "%d-%m-%Y %H:%M")
        valid_time_to = time.strptime(time_to, "%d-%m-%Y %H:%M")
    except ValueError:
        abort(415)
    response = {}
    counter = 0
    for document in repositories_data.find({
        "account": account, "repository": repository, "time": {"$lte": time_to, "$gte": time_from}
    }).sort("time"):
        response[counter] = {
            "account": document["account"],
            "repository": document["repository"],
            "time": document["time"]
        }
        counter += 1
    return (response, 200)

@app.route("/repos/delete/all", methods=['DELETE'])
def delete_all_repos():
    repositories_data.drop()
    return ({"delete all repositories": "OK"}, 200)

@app.route("/repos/delete", methods=['DELETE'])
def delete_repository():
    request_data = request.get_json()
    if len(request_data) != 2:
        abort(400)
    search_for_repository = repositories_data.find_one({"account": request_data['account'], "repository": request_data['repository']})
    if not search_for_repository:
        return ({"delete repository": "no such repository"}, 200)
    repositories_data.delete_many({"account": request_data['account'], "repository": request_data['repository']})
    return ({"delete account": "OK"}, 200)