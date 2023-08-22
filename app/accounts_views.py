import datetime
import time
import requests

from flask import request, abort
from .app import app
from .tools import create_account_change_response
from .models import accounts_data
from .parsing.account_parsing import AccountParse


@app.route("/accounts/add", methods=['POST'])
def add_new_account():
    request_data = request.get_json()
    if len(request_data) != 1 or not 'account' in request_data or request_data["account"] == "":
        abort(400)
    account = request_data["account"]
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    response = requests.get(f'http://github.com/{account}')
    if response.status_code != 200:
        abort(404)

    confirmed_account = AccountParse(account)
    try:
        new_document = {
            "account": account,
            "repositories_number": confirmed_account.get_repos_number(),
            "popular_repositories": confirmed_account.get_repos(),
            "followers": confirmed_account.get_followers(),
            "following": confirmed_account.get_following(),
            "contributions_last_year": confirmed_account.get_contributions_last_year(),
            "time": time_now
        }
    except:
        abort(404)
    accounts_data.insert_one(new_document)
    added_document = accounts_data.find_one({"time": time_now, "account": account})
    response = {
        "account": added_document["account"],
        "repositories_number": added_document["repositories_number"],
        "popular_repositories": added_document["popular_repositories"],
        "followers": added_document["followers"],
        "following": added_document["following"],
        "contributions_last_year": added_document["contributions_last_year"],
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
    response = requests.get(f'http://github.com/{account}')
    if response.status_code != 200:
        abort(response.status_code)
    try:
        valid_time_from = time.strptime(time_from, "%d-%m-%Y %H:%M")
        valid_time_to = time.strptime(time_to, "%d-%m-%Y %H:%M")
    except ValueError:
        abort(415)

    chosen_accounts = {}
    counter = 0
    for document in accounts_data.find({"account": account, "time": {"$lte": time_to, "$gte": time_from}}).sort("time"):
        chosen_accounts[counter] = {
            "account": document["account"],
            "repositories_number": document["repositories_number"],
            "popular_repositories": document["popular_repositories"],
            "followers": document["followers"],
            "following": document["following"],
            "contributions_last_year": document["contributions_last_year"],
            "time": document["time"]
        }
        counter += 1
    if counter == 0:
        return ({"get_stat": "no_changes_in_this_interval"}, 200)
    return (create_account_change_response(chosen_accounts[0], chosen_accounts[counter-1]), 200)


@app.route("/accounts/delete/all", methods=['DELETE'])
def delete_all_accounts():
    accounts_data.drop()
    return ({"delete_all_accounts": "OK"}, 200)


@app.route("/accounts/delete", methods=['DELETE'])
def delete_account():
    request_data = request.get_json()
    if len(request_data) != 1 or not 'account' in request_data:
        abort(400)

    search_for_account = accounts_data.find_one({"account": request_data['account']})
    if not search_for_account:
        abort(404)
    accounts_data.delete_many({"account": request_data['account']})
    return ({"delete_account": "OK"}, 200)
