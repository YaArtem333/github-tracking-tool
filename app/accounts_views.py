from flask import request, abort
from app.app import app
from app.models import accounts_data
import datetime


@app.route("/accounts/add", methods=['POST'])
def add_new_request():
    request_data = request.get_json()
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
def get_stat():
    account = request.args.get('account')
    time_from = request.args.get('from')
    time_to = request.args.get('to')
    response = {}
    counter = 0
    for document in accounts_data.find({"account": account, "time": {"$lte": time_to, "$gte": time_from}}):
        response[counter] = {
            "account": document["account"],
            "time": document["time"]
        }
        counter += 1
    return (response, 200)

@app.route("/accounts/delete/all", methods=['DELETE'])
def delete_all_data():
    accounts_data.drop()
    return ({"delete all data": "OK"}, 200)

@app.route("/accounts/delete", methods=['DELETE'])
def delete_account():
    request_data = request.get_json()
    search_for_account = accounts_data.find_one({"account": request_data['account']})
    accounts_data.delete_many({"account": request_data['account']})
    return ({"delete account": "OK"}, 200)
