Wargame server control
===========================
A Python 3 script for Wargame server automation

Features:
------------------
 - Enables you to implement custom logic on server events
 - Tracks current information about players on a server

Requirements:
-----------------
 - mcrcon
 - Python 3
 - Wargame series game

Usage:
------------------
 - Place it in the folder with your wargame server
 - Set up folder with json files that will be used as a settings
 - Run script giving the folder path (relative is ok) as a first parameter

JSON File description:
-------------------
 Description of JSON files and their contents
 
#### rcon.json:
 - `rconPath` - path to your rcon client
 - `rconRemoteHost` - IP address of your server
 - `rconRemotePort` - port for the rcon
 - `rconPassword` - password used for the client

#### defaults.json:
Certain server settings use enum values - noted as enum(int) - use only the int value 
 - `serverName` - Name of the Wargame lobby
 - `password` - password string to be used if you want the lobby to be password protected, leave blank if you don't want a password to be required
 - `gameMode` - setting the victory condition - Destruction(1), Economy(3), Conquest(4)
 - `alliances` - fighting sides - NATO vs PACT(0), NATO vs NATO(1), PACT vs PACT(2)
 - `maxPlayers` - overall limit of players in the lobby
 - `maxTeamSize` - limits the size of team per side
 - `playersToStart` - number of players required to start the countdown
 - `teamSizeDelta` - maximum player difference between teams(should prevent 10vs0 lobby situation)
 - `nationLimit` - Nation/Coalition deck limitation - None(-1), Nation or Coalition(0), Nation(1), Coalition(2)
 - `thematicLimit` - thematic deck limitation - None(-1), Any(-2), Motorised(0), Armored(1), Support(2), Marine(3), Mechanized(4), Airborne(5), Navy(6)
 - `dateLimit` - Year deck limitation - None(-1),  Pre85(0), Pre80(1)
 - `warmUpTime` - lobby countdown till game starts, cannot be less than 20
 - `loadingTime` - maximum lobby loading time - if a player fails to load into the game in the given interval, he will be kicked
 - `deploymentTime` - length of a in-game ready countdown
 - `debriefingTime` - length of a debrief time  
 
Principle of work:
-------------------
 - Script reads server log and finds the last line, when there was nobody on the server
 - Then it starts to accumulate information about present state, by analyzing later log entries
 - Each log line is compared with registered masks (in register_events) and, if matches, fires a service event handler
 - Service event handler updates internal information structures about current game state
 - When it finishes, the info gather run consider being passed (info_run = false)
 - From now on script opens log and reads logs newly written lines (if any)
 - Now, when log line is matched against the mask, service handler runs user handler after itself.
 - User handlers are supposed to contain functions that perform actions (so they will not be performed during information gathering)
 
Workflow:
-------------------
 - User operates, depending on the information about current state of the game 
 (gamestate var), players information (players dictionary, keys - player id) and information of event happened (handler function arguments)
 - User reacts with rcon commands via Rcon.execute()  
 - Several rcon commands are incapsulated in Player class, so user can just call player.change_deck() or player.kick()
 - Methods, that perform rcon operations are called change* to differ from set*
 - User code intended to be placed in functions in "Custom actions" section 
 
Notes:
------------------
 - Events are registered on the proxy service handlers to hide all service calculation, that user should not be bothered with. 
 If needed, event could be registered on user function directly