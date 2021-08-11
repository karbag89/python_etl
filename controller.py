import json
import requests

from error import Error


class Controller:

    def __init__(self, data, urls) -> None:
        self.v_count = data['count']
        self.accountId = data['accountId']
        self.playerName = data['name']
        self.url_recentMatches = urls['recentMatches']
        self.url_matches = urls['matches']

    def getTeam(self, players) -> bool:
        for player in players['players']:
            if player['account_id'] == self.accountId:
                v_team = player['isRadiant']
                return v_team

    def getTeamKills(self, matches, team) -> int:
        total_team_kills = 0
        for player in matches['players']:
            if player['isRadiant'] == team:
                total_team_kills += player.get('kills', 0)
        return total_team_kills

    def getPlayerKPIs(self) -> json:
        v_recent_matches = requests.get(self.url_recentMatches).json()

        if (isinstance(v_recent_matches, dict)
           and v_recent_matches.get('error', None) == 'Not Found'):
            return Error.errorMessage(500, "Internal Server Error! "
                                           "Please check the url.")
        if len(v_recent_matches) <= 0:
            return Error.errorMessage(404, "Player {} with account id {} "
                                           "not found!".format(self.playerName,
                                                               self.accountId))

        v_vars = {'max_kda': 0,
                  'min_kda': 0,
                  'avg_kda': 0,
                  'sum_kda': 0,
                  'max_kp': 0,
                  'min_kp': 0,
                  'avg_kp': 0,
                  'sum_kp': 0,
                  'curr_kills': 0,
                  'curr_assists': 0,
                  'game_count': 0,
                  'match_count': 0,
                  'team': True,
                  'total_team_kills': 0,
                  'total_count': 0}

        v_vars['total_count'] = len(v_recent_matches)

        if (self.v_count > v_vars['total_count']
           and v_vars['total_count'] > 0):
            self.v_count = v_vars['total_count']

        v_game_count = 0
        for data in v_recent_matches:
            v_game_count += 1

            if data.get('deaths', 0) == 0:
                data['deaths'] = 1

            v_curr_kills = data.get('kills', 0)
            v_curr_assists = data.get('assists', 0)

            v_current_kda = ((data.get('kills', 0) + data.get('assists', 0))
                             / data.get('deaths', 1))

            v_vars['sum_kda'] += v_current_kda

            if v_current_kda > v_vars.get('max_kda', 0):
                v_vars['max_kda'] = v_current_kda

            if v_current_kda < v_vars.get('min_kda', 0):
                v_vars['min_kda'] = v_current_kda

            if data.get('match_id', None) is None:
                return Error.errorMessage(404, "Match id for {} account id "
                                               "not found!"
                                               .format(self.accountId))

            url_matches = self.url_matches + str(data.get('match_id'))
            v_matches = requests.get(url_matches).json()

            if (isinstance(v_matches, dict)
               and v_matches.get('error', None) == 'Not Found'):
                return Error.errorMessage(500, "Internal Server Error. "
                                               "Please check the url.")

            v_vars['team'] = self.getTeam(v_matches)

            v_vars['total_team_kills'] = self.getTeamKills(v_matches,
                                                           v_vars['team'])

            v_current_kp = (((v_curr_kills + v_curr_assists)
                            / v_vars['total_team_kills']) * 100)

            v_vars['sum_kp'] += v_current_kp

            if v_current_kp > v_vars.get('max_kp', 0):
                v_vars['max_kp'] = v_current_kp

            if v_current_kp < v_vars.get('min_kp', 0):
                v_vars['min_kp'] = v_current_kp

            if v_game_count > self.v_count:
                break

        v_vars['avg_kda'] = v_vars.get('sum_kda', 1) / self.v_count
        v_vars['avg_kp'] = v_vars.get('sum_kp', 1) / self.v_count
        v_game = 'Dota'
        v_player_name = self.playerName
        v_totoal_games = self.v_count

        v_vars['max_kda'] = float('%.2f' % v_vars.get('max_kda'))
        v_vars['min_kda'] = float('%.2f' % v_vars.get('min_kda'))
        v_vars['avg_kda'] = float('%.2f' % v_vars.get('avg_kda'))

        v_vars['max_kp'] = str('%.2f' % v_vars.get('max_kp')) + "%"
        v_vars['min_kp'] = str('%.2f' % v_vars.get('min_kp')) + "%"
        v_vars['avg_kp'] = str('%.2f' % v_vars.get('avg_kp')) + "%"

        v_data_log = {
                        "game": v_game,
                        "player_name": v_player_name,
                        "total_games": v_totoal_games,
                        "max_kda": v_vars.get('max_kda', None),
                        "min_kda": v_vars.get('min_kda', None),
                        "avg_kda": v_vars.get('avg_kda', None),
                        "max_kp": v_vars.get('max_kp', None),
                        "min_kp": v_vars.get('min_kp', None),
                        "avg_kp": v_vars.get('avg_kp', None)
                    }

        json_response = json.dumps(v_data_log, indent=4)
        return json_response
