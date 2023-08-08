

def create_account_change_response(first_acc:dict, last_acc:dict):
    account = first_acc["account"]
    repositories_change = str(int(last_acc["repositories_number"]) - int(first_acc["repositories_number"]))
    if int(last_acc["repositories_number"]) - int(first_acc["repositories_number"]) > 0:
        repositories_change = "+" + str(int(last_acc["repositories_number"]) - int(first_acc["repositories_number"]))

    followers_change = str(int(last_acc["followers"]) - int(first_acc["followers"]))
    if int(last_acc["followers"]) - int(first_acc["followers"]) > 0:
        followers_change = "+" + str(int(last_acc["followers"]) - int(first_acc["followers"]))

    following_change = str(int(last_acc["following"]) - int(first_acc["following"]))
    if int(last_acc["following"]) - int(first_acc["following"]) > 0:
        following_change = "+" + str(int(last_acc["following"]) - int(first_acc["following"]))

    contributions_change = str(int(last_acc["contributions_last_year"]) - int(first_acc["contributions_last_year"]))
    if int(last_acc["contributions_last_year"]) - int(first_acc["contributions_last_year"]) > 0:
        contributions_change = "+" + str(int(last_acc["contributions_last_year"]) - int(first_acc["contributions_last_year"]))

    response = {
        "account": account,
        "repositories_number": last_acc["repositories_number"] + " " + f"({repositories_change})",
        "followers": last_acc["followers"] + " " + f"({followers_change})",
        "following": last_acc["following"] + " " + f"({following_change})",
        "contributions_last_year": last_acc["contributions_last_year"] + " " + f"({contributions_change})"
    }
    return response

