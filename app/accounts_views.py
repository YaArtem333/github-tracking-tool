import datetime
import time

from flask import request, abort
from .app import app
from .models import accounts_data


@app.route("/accounts/add", methods=['POST'])
def add_new_account():
    request_data = request.get_json()
    if len(request_data) != 1:
        abort(400)
    account = request_data["account"]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    new_document = {"account": account, "time": time_now}
    accounts_data.insert_one(new_document)

    added_document = accounts_data.find_one({"time": time_now, "account": account})
    response = {
        "account": added_document["account"],
        "time": added_document["time"]
    }
    return (response, 201)

@app.route("/accounts/stats", methods=['GET'])
def get_account_stat():
    account = request.args.get('account')
    time_from = request.args.get('from')
    time_to = request.args.get('to')
    if not time_from or not time_to or not account:
        abort(400)
    try:
        valid_time_from = time.strptime(time_from, "%d-%m-%Y %H:%M")
        valid_time_to = time.strptime(time_to, "%d-%m-%Y %H:%M")
    except ValueError:
        abort(415)
    response = {}
    counter = 0
    for document in accounts_data.find({"account": account, "time": {"$lte": time_to, "$gte": time_from}}).sort("time"):
        response[counter] = {
            "account": document["account"],
            "time": document["time"]
        }
        counter += 1
    return (response, 200)

@app.route("/accounts/delete/all", methods=['DELETE'])
def delete_all_accounts():
    accounts_data.drop()
    return ({"delete all accounts": "OK"}, 200)

@app.route("/accounts/delete", methods=['DELETE'])
def delete_account():
    request_data = request.get_json()
    if len(request_data) != 1:
        abort(400)
    search_for_account = accounts_data.find_one({"account": request_data['account']})
    if not search_for_account:
        return ({"delete account": "no such account"}, 200)
    accounts_data.delete_many({"account": request_data['account']})
    return ({"delete account": "OK"}, 200)
