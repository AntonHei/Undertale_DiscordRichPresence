# Undertale Discord Rich Presence
A Rich Presence Script for Undertale.

The script works with the savegames of **UNDERTALE**.
So every time you save, the stats will refesh after a period of time (every 10 seconds, adjustable in **config.ini**).

The script catches data like kills, playtime, deaths, LV, Room, Area and so on.
What the discord Presence shows can be setup in the **config.ini**, the current route (neutral or genocide), as well as the language, the refreshInterval and the Discord App ClientID.

# What it looks like #
![Neutral in snowdin](https://image.prntscr.com/image/OcQBms_cQ_iZbIDxMEcPPQ.png)<br>
or like this, if you are in a genocide run
<br>
![Genocide in snowdin](https://image.prntscr.com/image/WSzwFj26QkmHlfoIXdyMcQ.png)<br>
and this is what it looks like in closeup (text is customizable)
<br>
![Genocide in snowdin closeup](https://image.prntscr.com/image/tHB2n0oeRkK4GC_OifoNww.png)

# Documentation #
### config.ini ###
**discordAppClientID="674010865879744552"**
<br>
*Standard set as the official one by me, you can create your own and adress it*
<br>
<br>
**language="en"**
<br>
*Change this to the available ones in the "data" folder*
<br>
<br>
**refreshInterval="10"**
<br>
*The Interval the Discord Rich Presence will be updated*
<br>
<br>
**showRoute="True"**
<br>
*If this is True it will show the current Route with a small Picture in Discord*
<br>
### main_translations.json ###
In this file you can use these variable placeholders:
 - **{room_name}** - The name of the room the player is in (Room names are customizable in: "undertale_data.json")
 - **{room_area}** - The name of the Area the player is in (Area names are customizable in: "undertale_data.json")
  - **{room_area_code_name}** - The name of the Area the player is in (Area code names are customizable in: "undertale_data.json")
 - **{player_lv}** - The Player's LV, LOVE or Level of Violence
 - **{player_kills}** - The kill count of the player
 - **{player_deaths}** - The death count of the player
 - **{player_name}** - The name chosen at the begging of the game.
 - **{player_kills_ruins}** - The kill count of the player in the ruins area.
 - **{player_kills_snowdin}** - The kill count of the player in the snowdin area.
 - **{player_kills_waterfall}** - The kill count of the player in the waterfall area.
 - **{player_kills_hotland}** - The kill count of the player in the hotland area.
 - **{played_time}** - The played time, since last savegame (in Hours, round to 2 decimal places).
