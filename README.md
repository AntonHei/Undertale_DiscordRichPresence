# Undertale Discord Rich Presence
A Rich Presence Script for Undertale.

The script works with the savegames of **UNDERTALE**.
So every time you save, the stats will refesh after a period of time (every 10 seconds, adjustable in **config.ini**).

The script catches data like kills, playtime, deaths, LV, Room, Area and so on.
What the discord Presence shows can be setup in the **config.ini**, as well as the language, the refreshInterval and the Discord App ClientID.

# What it looks like #
![With big Area Logo](https://image.prntscr.com/image/EbN7iA1iTX_XohTgqYHQ1g.png)<br>
*or like this, if you change it so in the config.ini*
<br>
![With small Area Logo and Big Undertale Logo](https://image.prntscr.com/image/I6xIunX9TF6mkUPyUr33cQ.png)

# Documentation #
### config.ini ###
**areaBigLogo="True"**
<br>
*Change this to false to show the Undertale Logo as the big Picture and the area as the small Picture*
<br>
<br>
**discordAppClientID="674010865879744552"**
<br>
*Standard set as the official one by me, you can create your own and adress it*
<br>
<br>
**language="de"**
<br>
*Change this to the available ones in the "data" folder*
<br>
<br>
**refreshInterval="10"**
<br>
*The Interval the Discord Rich Presence will be updated*
<br>
### main_translations.json ###
In this file you can use these variable placeholders:
 - **{room_Name}** - The name of the room the player is in (Room names are customizable in: "undertale_data.json")
 - **{room_Area}** - The name of the Area the player is in (Area names are customizable in: "undertale_data.json")
 - **{player_LV}** - The Player's LV, LOVE or Level of Violence
 - **{player_kills}** - The kill count of the player
 - **{player_deaths}** - The death count of the player
 - **{player_name}** - The name chosen at the begging of the game.
 - **{played_time}** - The played time, since last savegame (in Hours, round to 2 decimal places).
