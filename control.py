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


class Game:
    """Main class, containing game process manipulation"""

    # -------------------------------------------
    # User event handlers
    # -------------------------------------------

    def on_player_connect(self, playerid):
        # self.no_battlegroups()  # rechecking the whoole lobby while only one player changed his deck - how exactly does the server operate? do i now what deck does the player has?
		pass

    def on_player_deck_set(self, playerid, playerdeck):
        self.no_battlegroup(playerid, playerdeck)

    def on_player_level_set(self, playerid, playerlevel):
        self.limit_level(playerid, playerlevel)

    def on_player_elo_set(self, playerid, playerelo):
        pass

    def on_player_side_change(self, playerid, playerside):
        pass

    def on_player_name_change(self, playerid, playername):
        pass

    def on_player_disconnect(self, playerid):
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

    def no_battlegroup(self, playerid, playerdeck):
        """rechecks ONE players deck and switches default battlegroups for custom genereal blue/red decks"""
        general_blue_deck = "@Hg6BiGNpaZEhRCvPizQIUgbkro85IwxgoZQ9UPRDOSkkd1AIJV0hFKTi+Au8sSQaUIxGPJn0ApLeKjSKBBNQ8UpQ"
        general_red_deck = "@Qs6CCYE6DFmdBC1BOzEBfQ1woQhoUItM9LWmYVAERnEDJCwQUketJeKVWkNATCaiYdARIsUS9E9RPETJG6R70Flo1CViDoA="
        blue_battlegroup = "@AMIBkNokCG0SBHHJAjjkgRxyQI4iZ2W5lxZhIT+E/Zb4WOFjRQCYkppJSwxckFJDCTYlgJeCoQlkJHkX4qfKSSq8qzKqwtArKRfgjYI/CyQrEo+JKmXA"
        red_battlegroup = "@QsIBiNcVhHCKwi1FYhagmQtQTEc56UHol5CaiYYoFIryBMgUJm4T6E8hLoS2Asg3GTJkyZMydclGJ6yfMI7CQQlYI1KZSP8iwISSbogK"
        if playerdeck == red_battlegroup:
            self.players[playerid].change_deck(general_red_deck)
            # self.players[playerid].change_deck_name("NM General Deck RED")
        if playerdeck == blue_battlegroup:
            self.players[playerid].change_deck(general_blue_deck)
            # self.players[playerid].change_deck_name("NM General Deck BLUE")
        if playerdeck == blue_battlegroup and self.players[playerid].get_side() == Side.Redfor:
            self.players[playerid].change_deck(general_red_deck)
            # self.players[playerid].change_deck_name("NM General Deck RED")
        if playerdeck == red_battlegroup and self.players[playerid].get_side() == Side.Bluefor:
            self.players[playerid].change_deck(general_blue_deck)
            # self.players[playerid].change_deck_name("NM General Deck BLUE")

    def map_random_rotate(self):
        """Rotate maps from the pool"""
        Server.change_map(self.map_pool[self.currentMapId])
        print("Rotating map to " + self.map_pool[self.currentMapId][0])
        self.currentMapId += 1
        if self.currentMapId == len(self.map_pool):
            self.currentMapId = 0
            random.shuffle(self.map_pool)

    def limit_level(self, playerid, playerlevel):
        """Kick players below certain level"""
        limit = 0
        if playerlevel < limit:
            print("Player level is too low: " + str(playerlevel) + ". Min is " + str(limit) + ". Kicking...")
            self.players[playerid].kick()

    # ----------------------------------------------------------------------------------------------------------------------
    # --------------------------------------- INTERNAL IMPLEMENTATION DETAILS ----------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------

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
        self.register_event('Entering in debriephing phase state', self._on_switch_to_debriefing)
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
		
	def setDefaultServerSettings(self, config):
		# TODO FILL THIS
		pass

    def main(self):
        print("Server control script started")
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

    def __init__(self, playerid):
        self._id = playerid
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

    def change_deck_name(self, deckname):
        """Renames players deck"""
        Rcon.execute("setpvar " + self._id + " PlayerDeckName " + deckname)

    def kick(self):
        """Kick player"""
        Rcon.execute("kick " + self._id)

    def ban(self):
        """Ban player"""
        Rcon.execute("ban " + self._id)


class Server:
    """
    Server data structure
    Incapsulates server manipulation
    """

    @classmethod
    def change_map(cls, mapsettings):
        Rcon.execute("setsvar NbMinPlayer 21")  # so that the game wont start
        Rcon.execute("setsvar Map " + mapsettings[0])
        Rcon.execute("setsvar TimeLimit " + mapsettings[1])
        Rcon.execute("setsvar InitMoney " + mapsettings[2])
        Rcon.execute("setsvar ScoreLimit " + mapsettings[3])
        Rcon.execute("setsvar IncomeRate " + mapsettings[4])
        Rcon.execute("setsvar NbMinPlayer 20")

    @classmethod
    def change_name(cls, name):
        Rcon.execute("setsvar ServerName " + name)


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
