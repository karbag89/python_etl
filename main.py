# ----------------------------------------------------------------------------
# Python library dependencies
# ----------------------------------------------------------------------------

from flask import Flask, request
from error import Error
from controller import Controller

app = Flask(__name__)


# The main function
def main():
    # Calling 'getKPIs' function to start the job.
    getKPIs()


# Handling error code 400 'Bad request!' response message.
@app.errorhandler(400)
def bad_request(e):
    return Error.errorMessage(400, "Bad Request! "
                                   "Please check input json parameters. ")


# Handling error code 404 'Page not found!' response message.
@app.errorhandler(404)
def page_not_found(e):
    return Error.errorMessage(404, "Page not found! "
                                   "Please check url. "
                                   "Example: ../players/top?count=11")


@app.post("/players/top")
def getKPIs():
    if request.is_json:
        # Getting top 'count' value from user input.
        try:
            count = int(request.args.get('count'))
        # Handling top 'count' user input value type.
        except (ValueError, TypeError):
            return Error.errorMessage(400, "Bad Request! "
                                           "Top n value must be "
                                           "only integer format. "
                                           "Example: ../players/top?count=11")
        # Getting player 'accountId' value from user input.
        try:
            accountId = request.get_json()["account_id"]
            # Handling player 'accountId' value type.
            if isinstance(accountId, bool):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a boolean.")
            # Handling player 'accountId' value type.
            if isinstance(accountId, float):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a float.")
            # Handling player 'accountId' value type.
            if isinstance(accountId, str):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a string.")

            # Getting player 'name' value from user input.
            playerName = request.get_json()["name"]
            # Handling player 'name' value type.
            if not isinstance(playerName, str):
                return Error.errorMessage(400, "User name not found! "
                                               "'name' must be string.")
            # Handling player 'name' value is empthy or not.
            elif len(playerName) == 0:
                return Error.errorMessage(404, "User name not found! "
                                               "The 'name' must not be empty "
                                               "string.")

        # Handling api response code 400 which is "Bad Request!".
        except KeyError:
            return Error.errorMessage(400, "Bad Request!")

        # Checking user input top value count.
        if count < 1:
            # Setting top 'count' variable to default 10 value.
            count = 10
        # Creating 'data' dictionary local variable which includes user input
        # variable.
        data = {'count': count,
                'accountId': accountId,
                'name': playerName}

        # Recent matches opendota api endpoint 'recentMatches_url' variable.
        recentMatches_url = 'https://api.opendota.com/api/players/{}' \
                            '/recentMatches'.format(accountId)
        # Matches opendota api endpoint 'matches_url' variable.
        matches_url = 'https://api.opendota.com/api/matches/'
        # Creating 'urls' dictionary local variable which includes opendota
        # api endpoints variables.
        urls = {'recentMatches': recentMatches_url,
                'matches': matches_url}

        # Calling Controller
        return Controller(data, urls).getPlayerKPIs()

    # Handling request type
    return Error.errorMessage(415, "Request must be json!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
