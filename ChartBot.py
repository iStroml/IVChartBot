import discord
from discord.ext import commands
import numpy as np
import json

bot = commands.Bot(command_prefix='!')
databasefile_base_cp = "datasets/basecp.json"
databasefile_pokedb = "datasets/pokemon_db.json"
pokedict = {}

startup_extensions = ["ServerMembers"]

#returns a dictionary of values for a specific pokemon. Checking for spelling mistakes with levenstein as well
def find_pkm(pkm_str):
    for pkm_id in pokedict:
        if (pkm_str == pkm_id):
            return pokedict[pkm_id]
        elif (pkm_str.lower() == pokedict[pkm_id]["ger_name"].lower() or pkm_str.lower() == pokedict[pkm_id]["en_name"].lower() or pkm_str.lower() == pokedict[pkm_id]["fr_name"].lower()):
            return pokedict[pkm_id]
    for pkm_id in pokedict:
        if(levenshtein(pkm_str.lower(), pokedict[pkm_id]["ger_name"].lower()) == 1 or levenshtein(pkm_str.lower(), pokedict[pkm_id]["en_name"].lower()) == 1):
            return pokedict[pkm_id]
    for pkm_id in pokedict:
        if(levenshtein(pkm_str.lower(), pokedict[pkm_id]["ger_name"].lower()) == 2 or levenshtein(pkm_str.lower(), pokedict[pkm_id]["en_name"].lower()) == 2):
            return pokedict[pkm_id]
    return {}


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def getivcombinations(min,max=None):

    #if no max value is given
    min = int(min)
    if (max != None):
        max = int(max)
    else:
        max = min

    #checking for wrong syntactical usage
    if min > max:
        tmp = max
        max = min
        min = tmp

    resultarray = []
    for attack in range(1, 16):
        for defense in range(1, 16):
            for stamina in range(1, 16):
                iv = round((attack + defense + stamina) / 45 * 100)
                if (iv <= max and iv >= min):
                    resultarray.append((attack,defense,stamina))
    return resultarray


#returns dictionary of CP values for a specific pokmeon based on its base stats
def compute_cp(base_atk, base_def, base_sta,iv_atk,iv_def, iv_sta):
    cp_multiplier = [
        0.09400000, 0.16639787, 0.21573247, 0.25572005, 0.29024988,
        0.32108760, 0.34921268, 0.37523559, 0.39956728, 0.42250001,
        0.44310755, 0.46279839, 0.48168495, 0.49985844, 0.51739395,
        0.53435433, 0.55079269, 0.56675452, 0.58227891, 0.59740001,
        0.61215729, 0.62656713, 0.64065295, 0.65443563, 0.66793400,
        0.68116492, 0.69414365, 0.70688421, 0.71939909, 0.73170000,
        0.73776948, 0.74378943, 0.74976104, 0.75568551, 0.76156384,
        0.76739717, 0.77318650, 0.77893275, 0.78463697, 0.79030001
    ]
    result = {}

    for lvl in range(1, 41):
        m = cp_multiplier[lvl - 1]
        attack = (int(base_atk) + int(iv_atk)) * m
        defense = (int(base_def) + int(iv_def)) * m
        stamina = (int(base_sta) + int(iv_sta)) * m
        cp = int(max(10, np.floor(np.sqrt(attack * attack * defense * stamina) / 10)))
        result[cp] = lvl
    return result



@bot.event
async def on_ready():
    print (bot.user.name + " connected")
    print ("With the ID: " + str(bot.user.id))
    activity = discord.Game(name="!help for help", type=0)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    #await bot.change_presence(game=discord.Game(name="!help for help", type=0))

#initialize_pokedict
with open(databasefile_pokedb, 'r') as database:
    pokedict = json.load(database)

#importing baseCPs
with open(databasefile_base_cp, 'r') as database:
    base_cp = json.load(database)
    for key in base_cp:
        pokedict[str(key)]["ATK"] = base_cp[key]["ATK"]
        pokedict[str(key)]["DEF"] = base_cp[key]["DEF"]
        pokedict[str(key)]["STA"] = base_cp[key]["STA"]


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run("yourtokengoeshere")
    bot.close()
