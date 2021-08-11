from flask import Flask, request
from controller import Controller

app = Flask(__name__)


def main():
    getKPIs()


@app.post("/players/top")
def getKPIs():
    if request.is_json:
        count = int(request.args.get('count'))
        accountId = request.get_json()["account_id"]
        playerName = request.get_json()["name"]

        data = {'count': count,
                'accountId': accountId,
                'name': playerName}

        recentMatches_url = 'https://api.opendota.com/api/players/{}' \
                            '/recentMatches'.format(accountId)

        matches_url = 'https://api.opendota.com/api/matches/'

        urls = {'recentMatches': recentMatches_url,
                'matches': matches_url}

        return Controller(data, urls).getPlayerKPIs()


if __name__ == "__main__":
    app.run()
