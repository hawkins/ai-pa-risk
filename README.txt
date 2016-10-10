RISK

risk.pyw

This game is relatively simple to play.  There are a few phases in the game.
1.  In pregame you create players.  

To create players, go to the Player menu and choose "New Player." You can type in a name, or, alternatively, click on "Set AI" and find the AI program you wish to use. Click ok when you're done with that.

Once you've created enough players, you can choose to start the game by clicking on "Start Game" under the player menu

The rest of the game proceeds by clicking on territories for placement, attacking, and fortification.

play_risk_ai.py

This will play a game between specified AIS. It can save the resulting logfiles out to the matches folder, with the logfile name including participating agent names and the time of the match.

usage: play_risk_ai.py [-h] [-n, --num NUM] [-w, --write] [-v, --verbose]
                       ais [ais ...]

Play a RISK match between some AIs

positional arguments:
  ais            List of the AIs for match: ai_1 name_1 ai_2 name_2 . . .

optional arguments:
  -h, --help     show this help message and exit
  -n, --num NUM  Specify the number of games each player goes first in match
  -w, --write    Indicate that logfiles should be saved to the matches
                 directory
  -v, --verbose  Indicate that the match should be run in verbose mode

This gives each player 10 minutes per match, and limits the match to 5000 actions.  The player that goes first will alternate each game.

risk_game_viewer

This will allow you to visually follow a match logfile.  

Usage: python risk_game_viewer.py LOGFILE.log

You can click next to step through the actions and states, or hit play to have it do it automatically.  The player and action information are displayed on the left of the screen. 



