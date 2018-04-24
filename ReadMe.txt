Setup
* Clone the repository and create your own discord bot (I won't explain this here, there are enough youtube tutorials for this step)
* Add your Bot token at the end of the ChartBot.py file bot.run("yourtokengoeshere")
* install the discord.py module. Python 3 and numpy are required as well (again, lots of tutorials are out there)
* specify your command prefix in ChartBot.py, default is "!"  (bot = commands.Bot(command_prefix='!') )
* navigate to the directory and run the python file using python3 ChartBot.py
* Add the bot to your discord and you should be fine

* If the setup fails - you can add MY bot to your local discord. Since this is non-profit I give no uptime-guarantee.
* There is no Icon As well since I dont want to get in license trouble with someone :P
https://discordapp.com/api/oauth2/authorize?client_id=438330961050992641&permissions=68608&scope=bot

Usage
* !cp or !wp Pokemonname Argument1 Argument2 Argument3
* !cp or !wp Pokemonname 15 15 14
* !cp or !wp Pokemonname 15 15 14-15
* !cp or !wp Pokemonname 100%
* !cp or !wp Pokemonname 90-100%
* !cp or !wp Bulbasaur  (shows a searchstring for 15 15 15 Bulbasaurs)
* !cp or !wp 1 15 15 15

The bot will tolerate some spelling mistakes. So Bulbazaur will be corrected to Bulbasaur - just in case.