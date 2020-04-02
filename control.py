#!/usr/local/bin/python3
# coding=utf-8
"""
 Wargame Server control script
 Author : DesertEagle
 Modified by : Sachy
"""

import re
import os
from time import sleep
from subprocess import call
from enum import Enum
from random import random
from math import floor
import json
import sys


class Rcon:
    """ Rcon connection settings """
    rconPath = "mcrcon"
    rconRemoteHost = "localhost"
    rconRemotePort = "14885"
    rconPassword = "password"

    @classmethod
    def execute(cls, command):
        """Execute rcon command, incapsulating details"""
        execution_string = cls.rconPath + ' -H ' + cls.rconRemoteHost + ' -P ' + cls.rconRemotePort + \
                           ' -p ' + cls.rconPassword + ' "' + command + '"'
        call(execution_string, shell=True)

    @classmethod
    def load_from_json(cls, path_to_json):
        """Loads class variables from the json provided in the variable"""
        print("Loading rcon information from " + path_to_json)
        with open(path_to_json + "/rcon.json", 'r') as json_file:
            parsed_json = json.load(json_file)
        Rcon.rconPath = parsed_json['rconPath']
        Rcon.rconPassword = parsed_json['rconPassword']
        Rcon.rconRemoteHost = parsed_json['rconRemoteHost']
        Rcon.rconRemotePort = parsed_json['rconRemotePort']


class Game:
    """Main class, containing game process manipulation"""

    # -------------------------------------------
    # User event handlers
    # -------------------------------------------

    def on_player_connect(self, playerid):
        # self.no_battlegroups()  # rechecking the whoole lobby while only one player changed his deck - how exactly does the server operate? do i now what deck does the player has?
        pass

    def on_player_deck_set(self, player_id, player_deck):
        self.no_battlegroup(player_id, player_deck)

    def on_player_level_set(self, player_id, player_level):
        self.limit_level(player_id, player_level)

    def on_player_elo_set(self, player_id, player_elo):
        pass

    def on_player_side_change(self, player_id, player_side):
        pass

    def on_player_name_change(self, player_id, player_name):
        pass

    def on_player_disconnect(self, player_id):
        pass

    def on_switch_to_game(self):
        pass

    def on_switch_to_debriefing(self):
        self.map_random_rotate()

    def on_switch_to_lobby(self):
        pass

    # -------------------------------------------
    # Custom actions
    # -------------------------------------------

    # Forcing certain deck usage
    def assign_decks(self):

        general_blue_deck = "XuAVOOkCbkxlBEyoMkgTf1Il1KtJYkaaQ9JaVnSbFS0syQUqwUlT/FVELI6A1nLhNYKTUsil9ScaLGLg"
        general_red_deck = "tOAcF6LTLwXEYZMocldI1qnDBZdjgqZZZKW4aUMuHEbSSRMWR2SyIWytaL9KelYE/A=="

        for playerID, player in self.players.items():
            if player.get_side() == Side.Bluefor:
                if player.get_deck() != general_blue_deck:
                    player.change_deck(general_blue_deck)

            if player.get_side() == Side.Redfor:
                if player.get_deck() != general_red_deck:
                    player.change_deck(general_red_deck)

    def no_battlegroups(self):
        """rechecks ALL players deck and switches default battlegroups for custom genereal blue/red decks"""
        general_blue_deck = "@Hg6BiGNpaZEhRCvPizQIUgbkro85IwxgoZQ9UPRDOSkkd1AIJV0hFKTi+Au8sSQaUIxGPJn0ApLeKjSKBBNQ8UpQ"
        general_red_deck = "@Qs6CCYE6DFmdBC1BOzEBfQ1woQhoUItM9LWmYVAERnEDJCwQUketJeKVWkNATCaiYdARIsUS9E9RPETJG6R70Flo1CViDoA="
        blue_battlegroup = "@AMIBkNokCG0SBHHJAjjkgRxyQI4iZ2W5lxZhIT+E/Zb4WOFjRQCYkppJSwxckFJDCTYlgJeCoQlkJHkX4qfKSSq8qzKqwtArKRfgjYI/CyQrEo+JKmXA"
        red_battlegroup = "@QsIBiNcVhHCKwi1FYhagmQtQTEc56UHol5CaiYYoFIryBMgUJm4T6E8hLoS2Asg3GTJkyZMydclGJ6yfMI7CQQlYI1KZSP8iwISSbogK"
        for playerID, player in self.players.items():
            if player.get_deck() == blue_battlegroup:
                player.change_deck(general_blue_deck)
                # self.players[playerID].change_deck_name("NM General Deck BLUE")
            if player.get_deck() == red_battlegroup:
                player.change_deck(general_red_deck)
                # self.players[playerID].change_deck_name("NM General Deck RED")
            if player.get_deck() == blue_battlegroup and self.players[playerID].get_side() == Side.Redfor:
                self.players[playerID].change_deck(general_red_deck)
                # self.players[playerID].change_deck_name("NM General Deck RED")
            if player.get_deck() == red_battlegroup and self.players[playerID].get_side() == Side.Bluefor:
                self.players[playerID].change_deck(general_blue_deck)
                # self.players[playerID].change_deck_name("NM General Deck BLUE")

    def no_battlegroup(self, player_id, player_deck):
        """rechecks ONE players deck and switches default battlegroups for custom genereal blue/red decks"""
        general_blue_deck = "@Hg6BiGNpaZEhRCvPizQIUgbkro85IwxgoZQ9UPRDOSkkd1AIJV0hFKTi+Au8sSQaUIxGPJn0ApLeKjSKBBNQ8UpQ"
        general_red_deck = "@Qs6CCYE6DFmdBC1BOzEBfQ1woQhoUItM9LWmYVAERnEDJCwQUketJeKVWkNATCaiYdARIsUS9E9RPETJG6R70Flo1CViDoA="
        blue_battlegroup = "@AMIBkNokCG0SBHHJAjjkgRxyQI4iZ2W5lxZhIT+E/Zb4WOFjRQCYkppJSwxckFJDCTYlgJeCoQlkJHkX4qfKSSq8qzKqwtArKRfgjYI/CyQrEo+JKmXA"
        red_battlegroup = "@QsIBiNcVhHCKwi1FYhagmQtQTEc56UHol5CaiYYoFIryBMgUJm4T6E8hLoS2Asg3GTJkyZMydclGJ6yfMI7CQQlYI1KZSP8iwISSbogK"
        if player_deck == red_battlegroup:
            self.players[player_id].change_deck(general_red_deck)
            # self.players[player_id].change_deck_name("NM General Deck RED")
        if player_deck == blue_battlegroup:
            self.players[player_id].change_deck(general_blue_deck)
            # self.players[player_id].change_deck_name("NM General Deck BLUE")
        if player_deck == blue_battlegroup and self.players[player_id].get_side() == Side.Redfor:
            self.players[player_id].change_deck(general_red_deck)
            # self.players[player_id].change_deck_name("NM General Deck RED")
        if player_deck == red_battlegroup and self.players[player_id].get_side() == Side.Bluefor:
            self.players[player_id].change_deck(general_blue_deck)
            # self.players[player_id].change_deck_name("NM General Deck BLUE")

    def map_random_rotate(self):
        """Rotate maps from the pool"""
        Server.change_map_settings(self.map_pool[self.currentMapId])
        print("Rotating map to " + self.map_pool[self.currentMapId][0])
        self.currentMapId += 1
        if self.currentMapId == len(self.map_pool):
            self.currentMapId = 0
            random.shuffle(self.map_pool)

    def limit_level(self, player_id, playe_rlevel):
        """Kick players below certain level"""
        limit = 0
        if playe_rlevel < limit:
            print("Player level is too low: " + str(playe_rlevel) + ". Min is " + str(limit) + ". Kicking...")
            self.players[player_id].kick()

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------------------- INTERNAL IMPLEMENTATION DETAILS ------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------
    # Service event handlers
    # -------------------------------------------

    def _on_player_connect(self, match_obj):

        playerid = match_obj.group(1)
        # Creating player data structure if not present
        if not (playerid in self.players):
            self.players[playerid] = Player(playerid)

        if not self.infoRun:
            self.on_player_connect(playerid)

    # ----------------------------------------------
    def _on_player_deck_set(self, match_obj):

        playerid = match_obj.group(1)
        playerdeck = match_obj.group(2)

        self.players[playerid].set_deck(playerdeck)

        if not self.infoRun:
            self.on_player_deck_set(playerid, playerdeck)

    # ----------------------------------------------
    def _on_player_level_set(self, match_obj):

        playerid = match_obj.group(1)
        playerlevel = match_obj.group(2)

        self.players[playerid].set_level(int(playerlevel))

        if not self.infoRun:
            self.on_player_level_set(playerid, int(playerlevel))

    # ----------------------------------------------
    def _on_player_elo_set(self, match_obj):

        playerid = match_obj.group(1)
        playerelo = match_obj.group(2)

        self.players[playerid].set_elo(float(playerelo))

        if not self.infoRun:
            self.on_player_elo_set(playerid, playerelo)

    # ----------------------------------------------
    def _on_player_disconnect(self, match_obj):

        playerid = match_obj.group(1)

        if not self.infoRun:
            self.on_player_disconnect(playerid)

        del self.players[playerid]

    # ----------------------------------------------
    def _on_player_side_change(self, match_obj):

        playerid = match_obj.group(1)
        playerside = match_obj.group(2)
        self.players[playerid].set_side(Side.Redfor if playerside == '1' else Side.Bluefor)

        if not self.infoRun:
            self.on_player_side_change(playerid, playerside)

    # ----------------------------------------------
    def _on_player_name_change(self, match_obj):

        playerid = match_obj.group(1)
        playername = match_obj.group(2)
        self.players[playerid].set_name(playername)

        if not self.infoRun:
            self.on_player_name_change(playerid, playername)

    # ----------------------------------------------
    def _on_switch_to_game(self, match_obj):
        self.gameState = GameState.Game

        if not self.infoRun:
            self.on_switch_to_game()

    # ----------------------------------------------
    def _on_switch_to_debriefing(self, match_obj):
        self.gameState = GameState.Debriefing

        if not self.infoRun:
            self.on_switch_to_debriefing()

    # ----------------------------------------------
    def _on_switch_to_lobby(self, match_obj):
        self.gameState = GameState.Lobby

        if not self.infoRun:
            self.on_switch_to_lobby()

    # ---------------------------------------------
    # Event handlers registration
    # ---------------------------------------------

    def register_events(self):
        self.register_event('Client added in session \(EugNetId : ([0-9]+)', self._on_player_connect)
        self.register_event('Client ([0-9]+) variable PlayerDeckContent set to "(.*)"', self._on_player_deck_set)
        self.register_event('Client ([0-9]+) variable PlayerLevel set to "(.*)"', self._on_player_level_set)
        self.register_event('Client ([0-9]+) variable PlayerElo set to "(.*)"', self._on_player_elo_set)
        self.register_event('Client ([0-9]+) variable PlayerAlliance set to "([0-9])"', self._on_player_side_change)
        self.register_event('Client ([0-9]+) variable PlayerName set to "(.*)"', self._on_player_name_change)
        self.register_event('Disconnecting client ([0-9]+)', self._on_player_disconnect)
        self.register_event('Entering in loading phase state', self._on_switch_to_game)
        self.register_event('Entering in debriefing phase state', self._on_switch_to_debriefing)
        self.register_event('Entering in matchmaking state', self._on_switch_to_lobby)

    # -------------------------------------------
    # Utility functions
    # -------------------------------------------

    def __init__(self):
        self.events = {}
        self.players = {}
        self.gameState = GameState.Lobby
        self.logfileStream = open("serverlog.txt", "r", encoding="utf-8")
        self.infoRun = True
        self.register_events()
        self.currentMapId = 0
        # (map, time_limit(seconds), init_money, score_target, income_rate(0-none <-->5-very high))
        self.map_pool = [("Destruction_2x2_port_Wonsan_Terrestre", "3000", "4000", "8000", "1"),
                         ("Destruction_2x3_Hwaseong", "3000", "4800", "8000", "1"),
                         ("Destruction_2x3_Esashi", "3000", "4500", "8000", "1"),
                         ("Destruction_3x3_Marine_3_Reduite_Terrestre", "3000", "4800", "8000", "1"),
                         ("Destruction_3x3_Muju_Alt", "3000", "4800", "8000", "1"),
                         ("Destruction_3x3_Muju", "3000", "4800", "8000", "1"),
                         ("Destruction_3x2_Montagne_3", "3000", "4800", "8000", "1"),
                         ("Destruction_2x3_Anbyon", "3000", "4800", "8000", "1"),
                         ("Destruction_2x3_Tohoku", "3000", "4800", "8000", "1"),
                         ("Destruction_3x2_Haenam_Alt", "3000", "4800", "8000", "1"),
                         ("Destruction_3x3_Marine_3_Terrestre", "3000", "5000", "8000", "1"),
                         ("Destruction_3x2_Boryeong_Terrestre", "3000", "4800", "8000", "1"),
                         ("Destruction_3x2_Taebuko", "3000", "4800", "8000", "1"),
                         ("Destruction_3x2_Sangju", "3000", "4800", "8000", "1"),
                         ("Destruction_2x3_Montagne_2", "3000", "4800", "8000", "1"),
                         ("Destruction_3x3_Pyeongtaek", "3000", "5000", "8000", "1"),
                         ("Destruction_3x3_Montagne_4", "3000", "5000", "8000", "1"),
                         ("Destruction_Chongju_Alt", "3000", "5000", "8000", "1"),
                         ("Destruction_3x3_Highway", "3000", "5000", "8000", "1"),
                         ("Destruction_3x2_Taean", "3000", "4800", "8000", "1"),
                         ("Destruction_3x3_Pyeongtaek_Alt", "3000", "5000", "8000", "1"),
                         ("Destruction_3x3_Thuringer_Wald", "3600", "5000", "8000", "1"),
                         ("Destruction_3x3_Thuringer_Wald_Alt", "3600", "5000", "8000", "1"),
                         ("Destruction_3x3_Montagne_1", "3600", "5000", "8000", "1"),
                         ("Destruction_4x3_Gjoll", "3600", "5000", "8000", "1"),
                         ("Destruction_4x3_Sangju_Alt", "3600", "5000", "8000", "1"),
                         ("Destruction_4x4_ThreeMileIsland", "3600", "5200", "8000", "1"),
                         ("Destruction_4x4_ThreeMileIsland_Alt", "3600", "5200", "8000", "1"),
                         ("Destruction_3x3_Asgard", "3600", "5000", "8000", "1"),
                         ("Destruction_3x3_Chongju", "3600", "5000", "8000", "1"),
                         ("Destruction_3x3_Gangjin", "3600", "5000", "8000", "1"),
                         ("Destruction_5x3_Marine_1_Alt", "3600", "5000", "8000", "1")
                         ]

        # Getting starting line
        while True:
            line = self.logfileStream.readline()
            if not line:
                # 0 player line is not found, reseting to the start of file
                self.logfileStream.seek(0, os.SEEK_SET)
                break

            if line == u"Variable NbPlayer set to \"0\"\n":
                # 0 player line is found, keeping this state of the stream
                break

    def __del__(self):
        self.logfileStream.close()

    @classmethod
    def set_default_server_settings(cls, path_to_json):
        print("Setting default server settings from " + path_to_json + "/defaults.json")
        with open(path_to_json + "/defaults.json", 'r') as json_file:
            parsed_json = json.load(json_file)
        Server.change_name(parsed_json["serverName"])
        Server.change_password(parsed_json["password"])
        Server.change_game_mode(parsed_json["gameMode"])
        Server.change_alliances(parsed_json["alliances"])
        Server.change_max_player(parsed_json["maxPlayers"])
        Server.change_max_team_size(parsed_json["maxTeamSize"])
        Server.change_required_players(parsed_json["playersToStart"])
        Server.change_team_delta(parsed_json["teamSizeDelta"])
        Server.change_nation_constraint(parsed_json["nationLimit"])
        Server.change_thematic_constraint(parsed_json["thematicLimit"])
        Server.change_date_constraint(parsed_json["dateLimit"])
        Server.change_warm_up_time(parsed_json["warmUpTime"])
        Server.change_loading_time(parsed_json["loadingTime"])
        Server.change_deployment_time(parsed_json["deploymentTime"])
        Server.change_debriefing_time(parsed_json["debriefingTime"])
        print("Defaults set.")

    def main(self):
        print("Server control script started")
        if sys.argv.__len__() < 2:
            print("Please run this script with a path to a folder with setting json files as a parameter.")
            return 2
        print("Starting to load data from JSONs")
        Rcon.load_from_json(sys.argv[1])
        Game.set_default_server_settings(sys.argv[1])
        
        print("Gather information run")

        self.update()

        print("Gather information run is over")
        self.infoRun = False
        # self.setDefaultServerSettings()

        print("Server control started")
        while True:
            self.update()
            if len(self.players) == 20 and self.gameState == GameState.Lobby:  # game should be in the countdown phase
                self.no_battlegroups()  # damage control for the battlegroup deck script
            sleep(0.5)

    def register_event(self, regex, handler):
        """Register event handler for a certain log entry"""
        self.events[re.compile(regex)] = handler

    def update(self):
        """Parse log and trigger event handler"""
        while True:
            line = self.logfileStream.readline()
            if line:
                # Test against event expressions
                for pair in self.events.items():
                    match = pair[0].match(line)
                    if match:
                        pair[1](match)
                        break
            else:
                break


class Player:
    """
    Player data structure
    Incapsulates player data manipulation
    """

    def __init__(self, player_id):
        self._id = player_id
        self._side = Side.Bluefor
        self._deck = ""
        self._level = 0
        self._elo = 0.0
        self._name = ""

    # Getters
    def get_id(self):
        return self._id

    def get_side(self):
        return self._side

    def get_deck(self):
        return self._deck

    def get_level(self):
        return self._level

    def get_elo(self):
        return self._elo

    def get_name(self):
        return self._name

    # Setters
    def set_side(self, side):
        self._side = side

    def set_deck(self, deck):
        self._deck = deck

    def set_level(self, level):
        self._level = level

    def set_elo(self, elo):
        self._elo = elo

    def set_name(self, name):
        self._name = name

    # ------------------------------
    # Manipulation logic for the player
    # ------------------------------

    def change_side(self, side):
        """Forcibly change player's side"""
        Rcon.execute("setpvar " + self._id + " PlayerAlliance " + str(side))

    def change_deck(self, deck):
        """Forcibly assign new deck to a player"""
        Rcon.execute("setpvar " + self._id + " PlayerDeckContent " + deck)

    def change_deck_name(self, deck_name):
        """Renames players deck"""
        Rcon.execute("setpvar " + self._id + " PlayerDeckName " + deck_name)

    def kick(self):
        """Kick player"""
        Rcon.execute("kick " + self._id)

    def ban(self):
        """Ban player"""
        Rcon.execute("ban " + self._id)


class Server:
    """
    Server data structure
    Encapsulates server manipulation
    """

    @classmethod
    def change_map_settings(cls, map_settings):
        Server.change_required_players(21)
        Server.change_map(map_settings[0])
        Server.change_time_limit(map_settings[1])
        Server.change_starting_points(map_settings[2])
        Server.change_victory_points(map_settings[3])
        Server.change_income_rate(map_settings[4])
        Server.change_required_players(20)

    @classmethod
    def change_map(cls, map_name):
        Rcon.execute("setsvar Map " + map_name)

    @classmethod
    def change_time_limit(cls, time):
        Rcon.execute("setsvar TimeLimit " + time)

    @classmethod
    def change_starting_points(cls, points):
        Rcon.execute("setsvar InitMoney " + points)

    @classmethod
    def change_victory_points(cls, points):
        Rcon.execute("setsvar ScoreLimit " + points)

    @classmethod
    def change_income_rate(cls, rate):
        Rcon.execute("setsvar IncomeRate " + rate)

    @classmethod
    def change_name(cls, name):
        Rcon.execute("setsvar ServerName " + name)

    @classmethod
    def change_password(cls, password):
        Rcon.execute("setsvar Password " + password)

    @classmethod
    def change_game_mode(cls, game_mode):
        Rcon.execute("setsvar VictoryCond " + game_mode)

    @classmethod
    def change_alliances(cls, alliances):
        Rcon.execute("setsvar GameType " + alliances)

    @classmethod
    def change_max_player(cls, max_player_count):
        Rcon.execute("setsvar NbMaxPlayer " + max_player_count)

    @classmethod
    def change_max_team_size(cls, max_team_size):
        Rcon.execute("setsvar MaxTeamSize " + max_team_size)

    @classmethod
    def change_required_players(cls, player_count):
        Rcon.execute("setsvar NbMinPlayer " + player_count)

    @classmethod
    def change_team_delta(cls, delta):
        Rcon.execute("setsvar DeltaMaxTeamSize " + delta)

    @classmethod
    def change_nation_constraint(cls, limit):
        Rcon.execute("setsvar NationConstraint " + limit)

    @classmethod
    def change_thematic_constraint(cls, limit):
        Rcon.execute("setsvar ThematicConstraint " + limit)

    @classmethod
    def change_date_constraint(cls, limit):
        Rcon.execute("setsvar DateConstraint " + limit)

    @classmethod
    def change_warm_up_time(cls, time):
        Rcon.execute("setsvar WarmupCountdown " + time)

    @classmethod
    def change_loading_time(cls, time):
        Rcon.execute("setsvar LoadingTimeMax " + time)

    @classmethod
    def change_deployment_time(cls, time):
        Rcon.execute("setsvar DeploiementTimeMax " + time)

    @classmethod
    def change_debriefing_time(cls, time):
        Rcon.execute("setsvar DebriefingTimeMax " + time)


class Side(Enum):
    Bluefor = 0
    Redfor = 1


class GameState(Enum):
    Lobby = 1
    Game = 2
    Debriefing = 3


# Starting everything
if __name__ == '__main__':
    Game().main()
