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

def create_repository_change_response(first_repo:dict, last_repo:dict):
    account = first_repo["account"]
    repository = first_repo["repository"]

    branches_change = str(int(last_repo["branches"]) - int(first_repo["branches"]))
    if int(last_repo["branches"]) - int(first_repo["branches"]) > 0:
        branches_change = "+" + str(int(last_repo["branches"]) - int(first_repo["branches"]))

    tags_change = str(int(last_repo["tags"]) - int(first_repo["tags"]))
    if int(last_repo["tags"]) - int(first_repo["tags"]) > 0:
        tags_change = "+" + str(int(last_repo["tags"]) - int(first_repo["tags"]))

    commits_change = str(int(last_repo["commits"]) - int(first_repo["commits"]))
    if int(last_repo["commits"]) - int(first_repo["commits"]) > 0:
        commits_change = "+" + str(int(last_repo["commits"]) - int(first_repo["commits"]))

    stars_change = str(int(last_repo["stars"]) - int(first_repo["stars"]))
    if int(last_repo["stars"]) - int(first_repo["stars"]) > 0:
        stars_change = "+" + str(int(last_repo["stars"]) - int(first_repo["stars"]))

    watching_change = str(int(last_repo["watching"]) - int(first_repo["watching"]))
    if int(last_repo["watching"]) - int(first_repo["watching"]) > 0:
        watching_change = "+" + str(int(last_repo["watching"]) - int(first_repo["watching"]))

    forks_change = str(int(last_repo["forks"]) - int(first_repo["forks"]))
    if int(last_repo["forks"]) - int(first_repo["forks"]) > 0:
        forks_change = "+" + str(int(last_repo["forks"]) - int(first_repo["forks"]))

    response = {
        "account": account,
        "repository": repository,
        "branches": last_repo["branches"] + " " + f"({branches_change})",
        "tags": last_repo["tags"] + " " + f"({tags_change})",
        "commits": last_repo["commits"] + " " + f"({commits_change})",
        "stars": last_repo["stars"] + " " + f"({stars_change})",
        "watching": last_repo["watching"] + " " + f"({watching_change})",
        "forks": last_repo["forks"] + " " + f"({forks_change})"
    }
    return response