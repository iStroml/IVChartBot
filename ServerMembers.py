import ChartBot

from discord.ext import commands


class ServerMembers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ivvalues(self,  pokemon, argument_1=None, argument_2=None, argument_3=None):
        ivcombinations = []
        currentpkm = ChartBot.find_pkm(pokemon)
        if currentpkm != {}:
            # Parsing empty arguments
            if argument_1 is None and argument_2 is None and argument_3 is None:
                ivcombinations.append((15, 15, 15))

            # Parsing specific iv
            elif argument_1 is not None and argument_2 is not None and argument_3 is not None:
                poss_atk = []
                poss_def = []
                poss_sta = []
                # Parsing eg 15 15 15
                if "-" not in argument_1 and "-" not in argument_2 and "-" not in argument_3:
                    ivcombinations.append((int(argument_1), int(argument_2), int(argument_3)))

                # Parsing eg 10-15 10-15 10-15
                else:
                    if "-" in argument_1:
                        for attack in range(int(argument_1.split("-")[0]), int(argument_1.split("-")[1]) + 1):
                            poss_atk.append(attack)
                    else:
                        poss_atk.append(int(argument_1))
                    if "-" in argument_2:
                        for defense in range(int(argument_2.split("-")[0]), int(argument_2.split("-")[1]) + 1):
                            poss_def.append(defense)
                    else:
                        poss_def.append(int(argument_2))
                    if "-" in argument_3:
                        for stamina in range(int(argument_3.split("-")[0]), int(argument_3.split("-")[1]) + 1):
                            poss_sta.append(stamina)
                    else:
                        poss_sta.append(int(argument_3))

                    for attack in poss_atk:
                        for defense in poss_def:
                            for stamina in poss_sta:
                                ivcombinations.append((attack, defense, stamina))

            # Parsing 90-100%
            elif "%" in argument_1 and "-" in argument_1 and len(argument_1.split("-")) == 2:
                argument_1 = argument_1.replace("%", "").split("-")
                ivcombinations = ChartBot.getivcombinations(argument_1[0], argument_1[1])

            # Parsing 90%
            elif "%" in argument_1 and argument_2 is None and argument_3 is None:
                argument_1 = argument_1.replace("%", "")
                ivcombinations = ChartBot.getivcombinations(argument_1)
            else:
                print("Syntax Error I guess.")

            # Get possible combinations
            cpchart = {}
            for triple in ivcombinations:
                pokemon_atk, pokemon_def, pokemon_sta = triple
                currentcpchart = ChartBot.compute_cp(currentpkm["ATK"],
                                                     currentpkm["DEF"],
                                                     currentpkm["STA"],
                                                     pokemon_atk, pokemon_def, pokemon_sta)
                for key in currentcpchart:
                    cpchart[key] = currentcpchart[key]

            # build resultstring
            resultstring = currentpkm["dex_no"].lstrip("0") + "&"
            for key in sorted(cpchart):
                resultstring = resultstring + "wp" + str(key) + ","
        else:
            return "I found no IV charts for your pokemon. Check the spelling and you will be fine."
        if "&" not in resultstring[:-1]:
            res = "Probably no IV combination possible or you messed up the syntax. Try:\n"
            "Bulbasaur 100%\n"
            "Bulbasaur 98-100%\n"
            "1 15 15 15\n"
            "Bulbasaur 15 14-15 15\n"
            return res
        else:
            return resultstring[:-1]

    def calcmaxdict(self, pokemon,level):
        currentpkm = ChartBot.find_pkm(pokemon)
        result = {}
        for attack in range(13, 16):
            for defense in range(13, 16):
                for stamina in range(13, 16):
                    currentcpchart = ChartBot.compute_cp(currentpkm["ATK"], currentpkm["DEF"],
                                                         currentpkm["STA"], attack, defense, stamina)
                    for key in currentcpchart:
                        if currentcpchart[key] == level:
                            iv = round((attack + defense + stamina) / 45 * 100)
                            result["(" + str(attack) + "," + str(defense) + "," + str(stamina) + ")"] = {"Max": key,"IV": str(iv) + "%"}
        return result

    @commands.command(brief='Generates a searchquery for the pokebox.', description='(Pokemonname Attack Defense Stamina)')
    async def wp(self, context, pokemon, argument_1=None, argument_2=None, argument_3=None):
        result = self.ivvalues(pokemon, argument_1, argument_2, argument_3)
        if len(result) > 2000:
            await context.send(result[:1999])
            await context.send(result[1999:])
        else:
            await context.send(result)

    @commands.command(brief='Generates a searchquery for the pokebox.', description='(Pokemonname Attack Defense Stamina)')
    async def cp(self, context, pokemon, argument_1=None, argument_2=None, argument_3=None):
        result = self.ivvalues(pokemon, argument_1, argument_2, argument_3)
        result = result.replace("w", "c")
        if len(result) > 2000:
            await context.send(result[:1999])
            await context.send(result[1999:])
        else:
            await context.send(result.replace("w", "c"))

    @commands.command(brief='Generates a MaxCP table for some any pokemon', description='(Pokemonname)')
    async def maxwp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon,40)
        resultstr = "(ATK,DEF,KP)\tMaxWP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key,value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + "WP \t"+str(maxdict[key]["IV"])+"\n"
        await context.send(resultstr)


    @commands.command(brief='Generates a MaxCP table for some any pokemon', description='(Pokemonname)')
    async def maxcp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon,40)
        resultstr = "(ATK,DEF,STA)\tMaxCP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key,value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + " CP\t"+str(maxdict[key]["IV"])+"\n"
        await context.send(resultstr)

    @commands.command(brief='Generates a Catch level 20 CP table for some any pokemon', description='(Pokemonname)')
    async def catchwp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon, 20)
        resultstr = "(ATK,DEF,KP)\tLvL20WP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key, value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + "WP \t" + str(maxdict[key]["IV"]) + "\n"
        await context.send(resultstr)

    @commands.command(brief='Generates a Catch lvl 20 CP table for some any pokemon', description='(Pokemonname)')
    async def catchcp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon, 20)
        resultstr = "(ATK,DEF,STA)\tLvL20CP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key, value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + " CP\t" + str(maxdict[key]["IV"]) + "\n"
        await context.send(resultstr)

    @commands.command(brief='Generates a Catch lvl 25 table for some any pokemon', description='(Pokemonname)')
    async def weathercatchwp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon, 25)
        resultstr = "(ATK,DEF,KP)\tLvL20WP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key, value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + "WP \t" + str(maxdict[key]["IV"]) + "\n"
        await context.send(resultstr)

    @commands.command(brief='Generates a Catch lvl 25 table for some any pokemon', description='(Pokemonname)')
    async def weathercatchcp(self, context, pokemon):
        maxdict = self.calcmaxdict(pokemon, 25)
        resultstr = "(ATK,DEF,STA)\tLvL20CP\t\t%\n----------------------\n"
        tmp_result = sorted(maxdict.items(), reverse=True)
        for key in tmp_result:
            key, value = key
            resultstr = resultstr + key + "\t\t" + str(maxdict[key]["Max"]) + " CP\t" + str(maxdict[key]["IV"]) + "\n"
        await context.send(resultstr)

def setup(bot):
    bot.add_cog(ServerMembers(bot))
