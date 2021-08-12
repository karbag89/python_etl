# ----------------------------------------------------------------------------
# Python library dependencies
# ----------------------------------------------------------------------------

import json
import requests
import time

from error import Error


# -------------------------------------------------------------------------
# Description :
# The Controller class getting player data in 2 JSON format files (accountId,
# name, count, urls), doing data manipulation/calculation, returning response
# message in JSON format.
#
# Parameters :
#     data    JSON format file including player account id, name, count values.
#     urls    JSON format file including opendota api endpoints.
#
# Return :
#     Log information message in JSON message format.
#
# -------------------------------------------------------------------------
class Controller:
    '''Takes JSON data and endpoint urls, returns response in JSON format.'''

    def __init__(self, data, urls) -> None:
        self.v_count = data['count']
        self.accountId = data['accountId']
        self.playerName = data['name']
        self.url_recentMatches = urls['recentMatches']
        self.url_matches = urls['matches']

    # -------------------------------------------------------------------------
    # Description :
    # This method getting current player data, returning player team value.
    #
    # Parameters :
    #     players     The json data including player data.
    #
    # Return :
    #     v_team       Returning the team value in boolean format.
    #
    # -------------------------------------------------------------------------
    def getTeam(self, players) -> bool:
        '''Takes current player data, returns player team value.'''
        for player in players['players']:
            if player['account_id'] == self.accountId:
                v_team = player['isRadiant']
                return v_team

    # -------------------------------------------------------------------------
    # Description :
    # This method getting current player data, returning player team total
    # kills value.
    #
    # Parameters :
    #     matches               Json data including player matches.
    #     team                  Player team.
    #
    # Return :
    #     v_total_team_kills    Returning total team kills in integer format.
    #
    # -------------------------------------------------------------------------
    def getTeamKills(self, matches, team) -> int:
        '''Takes current player data, returns player team total kills value.'''
        total_team_kills = 0
        for player in matches['players']:
            if player['isRadiant'] == team:
                total_team_kills += player.get('kills', 0)
        return total_team_kills

    # -------------------------------------------------------------------------
    # Description :
    # This method getting current player matches and returning appropriate
    # data which is including maximum, minimum and average KDA and KP values
    # also game, player name and totsl game count values.
    #
    # Return :
    #     json_response    Log information data in JSON messaage format.
    #
    # -------------------------------------------------------------------------
    def getPlayerKPIs(self) -> json:
        '''
            Getting current player matches and returning
            appropriate data which is including maximum, minimum and
            average KDA and KP values also game, player name and total
            game count values.
        '''
        v_start = time.time()
        v_recent_matches = requests.get(self.url_recentMatches).json()

        # Checking the recent matches variable is dict and contain value or
        # not.
        if (isinstance(v_recent_matches, dict)
           and v_recent_matches.get('error', None) == 'Not Found'):
            return Error.errorMessage(500, "Internal Server Error! "
                                           "Please check the url.")
        # Checking existence of player name and account id fields.
        if len(v_recent_matches) <= 0:
            return Error.errorMessage(404, "Player {} with account id {} "
                                           "not found!".format(self.playerName,
                                                               self.accountId))
        # Creating 'v_vars' dictionary local variable which includes variable
        # names with default values.
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

        # Getting total count of player recent matches.
        v_vars['total_count'] = len(v_recent_matches)

        # Checking the input top count value with total count of recent
        # matches if inputted value is greater than of total count of recent
        # matched, setting top count of matches to total count.
        if (self.v_count > v_vars['total_count']
           and v_vars['total_count'] > 0):
            self.v_count = v_vars['total_count']

        # Game count varible to control the execution of player recent
        # matches count.
        v_game_count = 0
        for data in v_recent_matches:
            v_game_count += 1

            # Setting deatrhs value to 1 to avoid 0 devision error.
            if data.get('deaths', 0) == 0:
                data['deaths'] = 1

            v_curr_kills = data.get('kills', 0)
            v_curr_assists = data.get('assists', 0)

            # Get current KDA value.
            v_current_kda = ((data.get('kills', 0) + data.get('assists', 0))
                             / data.get('deaths', 1))

            # Calculation of sum of KDA value.
            v_vars['sum_kda'] += v_current_kda

            # Getting maximum KDA value.
            if v_current_kda > v_vars.get('max_kda', 0):
                v_vars['max_kda'] = v_current_kda

            # Getting minimum KDA value.
            if v_current_kda < v_vars.get('min_kda', 0):
                v_vars['min_kda'] = v_current_kda

            # Checking exsistance of Match ID field value.
            if data.get('match_id', None) is None:
                return Error.errorMessage(404, "Match id for {} account id "
                                               "not found!"
                                               .format(self.accountId))
            # Getting game players information.
            url_matches = self.url_matches + str(data.get('match_id'))
            v_matches = requests.get(url_matches).json()

            # Checking the matches variable is dict and contain value or
            # not.
            if (isinstance(v_matches, dict)
               and v_matches.get('error', None) == 'Not Found'):
                return Error.errorMessage(500, "Internal Server Error. "
                                               "Please check the url.")

            # Getting player team.
            v_vars['team'] = self.getTeam(v_matches)

            # Getting player team Total kills.
            v_vars['total_team_kills'] = self.getTeamKills(v_matches,
                                                           v_vars['team'])

            # Get current KP value
            v_current_kp = (((v_curr_kills + v_curr_assists)
                            / v_vars['total_team_kills']) * 100)

            # Calculation of sum of KP value.
            v_vars['sum_kp'] += v_current_kp

            # Getting maximum KP value.
            if v_current_kp > v_vars.get('max_kp', 0):
                v_vars['max_kp'] = v_current_kp

            # Getting minimum KP value.
            if v_current_kp < v_vars.get('min_kp', 0):
                v_vars['min_kp'] = v_current_kp

            # Terminating for loop when game count was reached.
            if v_game_count > self.v_count:
                break

        # Calculation of appropriate parameters.
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

        v_end = time.time()
        # Calculation of task duration value in seconds.
        v_duration = str('%.2f' % (v_end - v_start)) + " sec"

        # Preparing log information message body.
        v_data_log = {
                        "game": v_game,
                        "player_name": v_player_name,
                        "total_games": v_totoal_games,
                        "task_duration": v_duration,
                        "max_kda": v_vars.get('max_kda', None),
                        "min_kda": v_vars.get('min_kda', None),
                        "avg_kda": v_vars.get('avg_kda', None),
                        "max_kp": v_vars.get('max_kp', None),
                        "min_kp": v_vars.get('min_kp', None),
                        "avg_kp": v_vars.get('avg_kp', None)
                    }
        # Log information data in JSON messaage format.
        json_response = json.dumps(v_data_log, indent=4)
        return json_response
