from flask import Flask, request
from error import Error
from controller import Controller

app = Flask(__name__)


def main():
    getKPIs()


@app.post("/players/top")
def getKPIs():
    if request.is_json:
        try:
            count = int(request.args.get('count'))
        except (ValueError, TypeError):
            return Error.errorMessage(400, "Bad Request! "
                                           "Top n value must be "
                                           "only integer format. "
                                           "Example: ../players/top?count=11")
        try:
            accountId = request.get_json()["account_id"]
            if isinstance(accountId, bool):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a boolean.")
            if isinstance(accountId, float):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a float.")
            if isinstance(accountId, str):
                return Error.errorMessage(400, "Bad Request! "
                                               "'account_id' must be "
                                               "integer, not a string.")

            playerName = request.get_json()["name"]
            if not isinstance(playerName, str):
                return Error.errorMessage(400, "User name not found! "
                                               "'name' must be string.")
            elif len(playerName) == 0:
                return Error.errorMessage(404, "User name not found! "
                                               "The 'name' must not be empty "
                                               "string.")

        except KeyError:
            return Error.errorMessage(400, "Bad Request!")

        if count < 1:
            count = 10

        data = {'count': count,
                'accountId': accountId,
                'name': playerName}

        recentMatches_url = 'https://api.opendota.com/api/players/{}' \
                            '/recentMatches'.format(accountId)
        matches_url = 'https://api.opendota.com/api/matches/'

        urls = {'recentMatches': recentMatches_url,
                'matches': matches_url}

        return Controller(data, urls).getPlayerKPIs()

    return Error.errorMessage(415, "Request must be json!")


if __name__ == "__main__":
    app.run()
