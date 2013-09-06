Citadels
==============

A python implementation of the card game [Citadels](#http://en.wikipedia.org/wiki/Citadels_%28card_game%29) by Bruno Faidutti.

Installation
--------------
To install, run '.\install.sh' on Linux or 'install.bat' on Windows. This will create a virtual environment in the project directory and install required packages. This will activate the virtual environment. To deactivate, run 'deactivate'. To reactivate the environment run 'source env/bin/activate' on Linux or 'env\Scripts\activate' on Windows.

Run
--------------
To run the program, activate the environment and run 'python server.py'

Author
--------------
Christopher Mohr

Card Description
--------------
Included here are shot description of cards (roles and purple districts). All of this will eventually be included in game.

### Roles ###
####1 - Assassin####
Choose a character you want murder. They skip their entire turn and say nothing.

####2 - Thief####
Choose a character you want to steal from. When they take their turn, you first take all their gold. You cannot steal from the Assassin or the Assassin's target.

####3 - Magician####
Once during your turn, you may do one of the following
* Exchange your hand for that of another player.
* Place any number of cards from your hand on the bottom of the District Deck, then draw that many cards.

####4 - King####
Once during your turn, you may receive one gold for each noble (yellow) district in your city.
When the King is called, you recieve the Crown and are now the starting player for character selection until another player is called King.
If you are murdered, you receive the Crown at the end of the turn.

####5 - Bishop####
Once during your turn, you may receive one gold for each religious (blue) district in your city.
Your districts may not be destroyed by the Warlord

####6 - Merchant####
Once during your turn, you may receive one gold for each trade (green) district in your city.
After you take an action, you receive one gold

####7 - Architect####
After you take an action, you draw additional district cards
You may build up to three districts during your turn.

####8 - Warlord####
Once during your turn, you may receive one gold for each military (red) district in your city.
At the end of your turn, you may destroy a district of your choice by paying gold equal to one less than its cost. You may not destroy a district in a city that is already completed by having eight districts.

### Purple Districts ###
####Haunted City - 2 gold####
For the purposes of scoring, the Haunted City is considered to be the color of your choice. You cannot use this ability if you build it during the last round of the game.

####Keep - 3 gold####
The Keep cannot be destroyed by the Warlord.

####Laboratory - 5 gold####
Once during your turn, you may discard a card from your hand and receive one gold.

####Smithy - 5 gold####
Once during your turn, you may pay three gold to draw two district cards.

####Observatory - 5 gold####
If you choose to draw cards when you take an action, you draw three cards and keep one of your choice

####Graveyard - 5 gold####
When the Warlord destroys a district, you may pay one gold to take the destroyed district into your hand. You man not use this ability if you are the Warlord.

####Dragon Gate - 6 gold####
This district cost 6 gold to build, but is worth 8 points at the end of the game.

####University - 6 gold####
This district cost 6 gold to build, but is worth 8 points at the end of the game.

####Library - 6 gold####
If you choose to draw cards when you take an action, you may keep two of the cards you have drawn.

####Great Wall - 6 gold####
The cost for the Warlord to destroy any of your other districts in increased by one gold.

####School of Magic - 6 gold####
For the purposes of income, The School of Magic is considered to be the color of your choice.
