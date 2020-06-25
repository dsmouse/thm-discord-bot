import json

import requests

import libs.config as config

####################
# Config variables #
####################

c_api_rank = config.get_config("url")["api"]["user"]
c_api_token = config.get_config("url")["api"]["token"]
c_api_leaderboard = config.get_config("url")["api"]["leaderboard"]
c_url_userprofile = config.get_config("url")["user_profile"]

#############
# Functions #
#############


def get_user_data(username):
    """Fetches the user's data."""

    response = requests.get(
        c_api_rank.format(username))
    data = response.text
    return json.loads(data)


def get_sub_status(username):
    """Fetches the user's sub status."""

    url = c_url_userprofile.format(username)
    check = "No!"
    try:
        response = requests.get(url)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        if "<span>Subscribed</span>" in response.text:
            check = "Yes!"
        else:
            check = "No!"
    return check


pages = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25, 6: 30, 7: 35, 8: 40, 9: 45, 10: 50}


def get_leaderboard_data(page, monthly: bool = False):
    leaderboard_type = "topUsersMonthly" if monthly else "topUsers"

    response = requests.get(c_api_leaderboard)
    data = response.text
    data = json.loads(data)[leaderboard_type]
    num = pages[page] - 5

    return data[num:pages[page]]
