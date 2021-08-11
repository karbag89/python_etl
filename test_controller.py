import json

from controller import Controller

data = {'count': 10,
        'accountId': 639740,
        'name': "YrikGood"}

recentMatches_url = 'https://api.opendota.com/api/players/{}' \
                    '/recentMatches'.format(639740)

matches_url = 'https://api.opendota.com/api/matches/'

urls = {'recentMatches': recentMatches_url,
        'matches': matches_url}

v_data_players = {
   "match_id": 6126666493,
   "radiant_win": True,
   "players": [
      {
         "match_id": 6126666493,
         "account_id": 639740,
         "assists": 5,
         "deaths": 3,
         "kills": 4,
         "isRadiant": True
      },
      {
         "match_id": 6126666493,
         "account_id": 77719329,
         "assists": 7,
         "deaths": 6,
         "kills": 23,
         "isRadiant": True
      },
      {
         "match_id": 6126666493,
         "account_id": "None",
         "assists": 3,
         "deaths": 3,
         "kills": 10,
         "isRadiant": False
      }
   ],
   "patch": 48,
   "region": 8,
   "replay_url": "http://replay188.valve.net/570/6126666493_52464073.dem.bz2"
}

v_json = {'game': 'Dota',
          'player_name': 'YrikGood',
          'total_games': 10,
          'max_kda': 18.0,
          'min_kda': 0.0,
          'avg_kda': 4.82,
          'max_kp': '77.78%',
          'min_kp': '0.00%',
          'avg_kp': '57.88%'
          }


def test_getTeam():
    controller_obj = Controller(data, urls)
    assert controller_obj.getTeam(v_data_players)


def test_getTeamKills():
    controller_obj = Controller(data, urls)
    assert controller_obj.getTeamKills(v_data_players, True) == 27


def test_getPlayerKPIs():
    controller_obj = Controller(data, urls)
    v_data = json.loads(controller_obj.getPlayerKPIs())
    assert v_data == v_json
