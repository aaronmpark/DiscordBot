import discord
import responses
import random
from discord.ext import commands
from discord.app_commands import Choice
from discord import app_commands
import aiohttp
import openai
from riotwatcher import LolWatcher, ApiError
import requests
from config import TOKEN, RIOTAPI, spotifyClientID, spotifyClientSecret, client_ID, client_secret, openai_api_key

openai.api_key = openai_api_key

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        await bot.process_commands(message)

    @bot.event
    async def sync():
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}!",
                                                ephemeral=True)

    @bot.tree.command(name="roll")
    async def roll(interaction: discord.Interaction):
        await interaction.response.send_message(str(random.randint(1, 100)))

    @bot.tree.command(name="announce")
    async def announce(interaction: discord.Interaction, header: str, title: str, url: str, description: str, channel: str):
        embed = discord.Embed(title = title, url = url, description= description)
        link = url[url.index("=")+1:]
        embed.set_image(url = "https://i.ytimg.com/vi/"+link+"/maxresdefault.jpg")
        embed.set_author(name = header)
        await interaction.response.send_message("Sent!")
        my_channel = await bot.fetch_channel(channel)
        await my_channel.send(embed = embed)

    @bot.tree.command(description = 'ask me a question')
    async def ask(interaction: discord.Interaction, message: str):
        ret = ""
        try:
            await interaction.response.defer()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a chatbot that assists any questions that the user requests."},
                    {"role": "user", "content": message}
                ]
            )
            ret = response.choices[0].message['content']

        except openai.error.RateLimitError as e:
            ret = "Sorry, I've reached my response limit. Please try again later."
        except openai.error.OpenAIError as e:
            ret = f"An error occurred: {str(e)}"
        
        print(ret)
        try:
            await interaction.followup.send(ret)
        except discord.errors.NotFound as e:
            print(f"Failed to send follow-up message: {e}")

        
    @app_commands.choices(weapon = [
        Choice(name = 'gun', value = 'gun'),
        Choice(name='rock', value='rock'),
        Choice(name='sword', value='sword')
    ])
    @bot.tree.command(description = 'pick weapon')
    async def pick(interaction: discord.Interaction, weapon:str):
        number = random.randint(0,2)
        if weapon == 'gun' and number == 0:
            await interaction.response.send_message('The opponent chose rock! You win!')
        if weapon == 'gun' and number == 1:
            await interaction.response.send_message('The opponent chose sword! The opponent deflected your bullet! You lose!')
        if weapon == 'gun' and number == 2:
            await interaction.response.send_message('The opponent chose gun! Draw!')
        elif weapon == 'rock' and number == 0:
            await interaction.response.send_message('The opponent chose sword! You win!')
        elif weapon == 'rock' and number == 1:
            await interaction.response.send_message('The opponent chose rock! Draw!')
        elif weapon == 'rock' and number == 2:
            await interaction.response.send_message('The opponent chose gun! The opponent shot you before you could throw your rock. You lose!')
        elif weapon == 'sword' and number == 0:
            await interaction.response.send_message('The opponent chose gun! You deflected the bullet. You win!')
        elif weapon == 'sword' and number == 1:
            await interaction.response.send_message('The opponent chose rock! Your sword was useless. You lose!')
        elif weapon == 'sword' and number == 2:
            await interaction.response.send_message('The opponent chose sword! Draw!')


    @bot.command()
    async def dog(ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                res = await r.json()
                em = discord.Embed(title = "Random Dog Pictures!")
                em.set_image(url=res['message'])
                await ctx.send(embed=em)
    
    @bot.command(name="commands")
    async def commands(ctx):
        embed = discord.Embed(
        title= 'Bot Commands',
        description='List of all KAPNOYR commands \n-------------------------------------------------------------------',
        color= discord.Color.green()
    )
        embed.set_thumbnail(url='https://images.sftcdn.net/images/t_app-icon-m/p/2f29be38-96d7-11e6-abcb-00163ed833e7/2346725557/osu-icon.png')

        embed.add_field(name="- /opgg [Summoner Name] | $opgg [Summoner Name]",value='Returns the League of Legends Ranked Data for the Summoner',inline=False)
        embed.add_field(name="- /announce [header, title, url, description, channel]",value='Returns an embed of a YouTube video to a specific channel',inline=False)
        embed.add_field(name="- /ask ",value='KAPNOYR bot sends an AI-generated response to any message provided',inline=False)
        embed.add_field(name="- /pick [weapon]",value='KAPNOYR bot plays a modified game of rock-paper-scissors with you',inline=False)
        embed.add_field(name="- /dog | $dog",value='Returns an embed of random cute dog photos!',inline=False)
        embed.add_field(name="- /roll",value='Rolls a random number from 0-100',inline=False)
        embed.add_field(name="- /embeder [header, title, description, channel]",value='Returns an embed of the specified quantities into the specified channel',inline=False)
        embed.add_field(name="- !ping",value='Returns the bot latency (ms) ',inline=False)

        await ctx.send(embed = embed)
    
    @bot.tree.command(name="dog")
    async def dog(interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as r:
                res = await r.json()
                em = discord.Embed(title = "Random Dog Pictures!")
                em.set_image(url=res['message'])
                await interaction.response.send_message(embed=em)

    @bot.command()
    async def ping(ctx):
        await ctx.reply(f"Pong! The bot is running at {round(bot.latency*1000)} ms")

    @bot.command()
    async def waifu(ctx, type, category):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/"+type+"/"+category) as r:
                res = await r.json()
                em = discord.Embed(title = type)
                em.set_author(name = category)
                em.set_image(url=res['url'])
                await ctx.send(embed=em)

    @bot.tree.command(name="embeder")
    async def Embeder(interaction: discord.Interaction, header: str, title: str, description: str, channel: str):
        embed = discord.Embed(title = title, description= description)
        embed.set_author(name = header)
        await interaction.response.send_message("Sent!")
        my_channel = await bot.fetch_channel(channel)
        await my_channel.send(embed = embed)


    @bot.command()
    async def opgg(ctx, name): 
        RIOTAPI = "RGAPI-e14f11fe-b28e-4a8c-8ae0-c89d122c5da9"
        watcher = LolWatcher(RIOTAPI)
        me = watcher.summoner.by_name('na1', name)
        ranked_stats = watcher.league.by_summoner('na1', me['id'])
        print(ranked_stats)

        if len(ranked_stats) == 2:
            flex_stats = ranked_stats[0]
            solo_stats = ranked_stats[1]
            for each in solo_stats:
                if each == 'tier':
                    solo_rank = solo_stats[each]
                if each == 'rank':
                    solo_rank = solo_rank + ' ' + solo_stats[each]
                if each == 'wins':
                    solo_wins = str(solo_stats[each])
                if each == 'losses':
                    solo_losses = str(solo_stats[each])
                if each == 'leaguePoints':
                    solo_LP = str(solo_stats[each])
            solo_ratio = str(int(int(solo_wins)/(int(solo_wins)+int(solo_losses)) * 100))
            for each in flex_stats:
                if each == 'tier':
                    flex_rank = flex_stats[each]
                if each == 'rank':
                    flex_rank = flex_rank + ' ' + flex_stats[each]
                if each == 'wins':
                    flex_wins = str(flex_stats[each])
                if each == 'losses':
                    flex_losses = str(flex_stats[each])
                if each == 'leaguePoints':
                    flex_LP = str(flex_stats[each])
            flex_ratio = str(int(int(flex_wins)/(int(flex_wins)+int(flex_losses)) * 100))
            em = discord.Embed(title=name, url = "https://www.op.gg/summoners/na/"+name, description= "Ranked Solo: "+ solo_rank + ', ' + solo_wins+"W/"+solo_losses+"L, Win Rate: "+solo_ratio+ " LP: "+solo_LP+
                                                                                                "\nRanked Flex: "+ flex_rank + ', ' + flex_wins+"W/"+flex_losses+"L, Win Rate: "+flex_ratio+ " LP: "+flex_LP)
            em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
        elif len(ranked_stats) == 1:
            if ranked_stats[0]['queueType'] == 'RANKED_FLEX_SR':
                flex_stats = ranked_stats[0]
                for each in flex_stats:
                    if each == 'tier':
                        flex_rank = flex_stats[each]
                    if each == 'rank':
                        flex_rank = flex_rank + ' ' + flex_stats[each]
                    if each == 'wins':
                        flex_wins = str(flex_stats[each])
                    if each == 'losses':
                        flex_losses = str(flex_stats[each])
                    if each == 'leaguePoints':
                        flex_LP = str(flex_stats[each])
                flex_ratio = str(int(int(flex_wins)/(int(flex_wins)+int(flex_losses)) * 100))
                em = discord.Embed(title=name, url = "https://www.op.gg/summoners/na/"+name, description= "Ranked Solo: UNRANKED, LP: 0"+
                "\nRanked Flex: "+ flex_rank + ', ' + flex_wins+"W/"+flex_losses+"L, Win Rate: "+flex_ratio+ " LP: "+flex_LP)
                em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
            if ranked_stats[0]['queueType'] == 'RANKED_SOLO_5x5':
                solo_stats = ranked_stats[0]
                for each in solo_stats:
                    if each == 'tier':
                        solo_rank = solo_stats[each]
                    if each == 'rank':
                        solo_rank = solo_rank + ' ' + solo_stats[each]
                    if each == 'wins':
                        solo_wins = str(solo_stats[each])
                    if each == 'losses':
                        solo_losses = str(solo_stats[each])
                    if each == 'leaguePoints':
                        solo_LP = str(solo_stats[each])
                solo_ratio = str(int(int(solo_wins)/(int(solo_wins)+int(solo_losses)) * 100))
                em = discord.Embed(title=name, url = "https://www.op.gg/summoners/na/"+name, description= "Ranked Solo: "+ solo_rank + ', ' + solo_wins+"W/"+solo_losses+"L, Win Rate: "+solo_ratio+ " LP: "+solo_LP+ "\nRanked Flex: UNRANKED, LP: 0")
                em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
        else:
            em = discord.Embed(title=name, url = "https://www.op.gg/summoners/na/"+name, description= "Ranked Solo: UNRANKED, LP: 0" + "\nRanked Flex: UNRANKED, LP: 0")
            em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")

        await ctx.send(embed=em)


    @bot.tree.command(name = "opgg")
    async def opgg(interaction: discord.Interaction, name: str):
        if " " in name:
            write_name = name[:name.find(" ")] + "%20"+ name[name.find(" ")+1: ]
            title_name = name[:name.find(" ")] + " "+ name[name.find(" ")+1: ]
        else:
            write_name = name
            title_name = name
        watcher = LolWatcher(RIOTAPI)
        me = watcher.summoner.by_name('na1', name)
        ranked_stats = watcher.league.by_summoner('na1', me['id'])

        if len(ranked_stats) == 2:
            flex_stats = ranked_stats[0]
            solo_stats = ranked_stats[1]
            for each in solo_stats:
                if each == 'tier':
                    solo_rank = solo_stats[each]
                if each == 'rank':
                    solo_rank = solo_rank + ' ' + solo_stats[each]
                if each == 'wins':
                    solo_wins = str(solo_stats[each])
                if each == 'losses':
                    solo_losses = str(solo_stats[each])
                if each == 'leaguePoints':
                    solo_LP = str(solo_stats[each])
            solo_ratio = str(int(int(solo_wins)/(int(solo_wins)+int(solo_losses)) * 100))
            for each in flex_stats:
                if each == 'tier':
                    flex_rank = flex_stats[each]
                if each == 'rank':
                    flex_rank = flex_rank + ' ' + flex_stats[each]
                if each == 'wins':
                    flex_wins = str(flex_stats[each])
                if each == 'losses':
                    flex_losses = str(flex_stats[each])
                if each == 'leaguePoints':
                    flex_LP = str(flex_stats[each])
            flex_ratio = str(int(int(flex_wins)/(int(flex_wins)+int(flex_losses)) * 100))
            em = discord.Embed(title=title_name, url = "https://www.op.gg/summoners/na/"+write_name, description= "Ranked Solo: "+ solo_rank + ', ' + solo_wins+"W/"+solo_losses+"L, Win Rate: "+solo_ratio+ " LP: "+solo_LP+
                                                                                                "\nRanked Flex: "+ flex_rank + ', ' + flex_wins+"W/"+flex_losses+"L, Win Rate: "+flex_ratio+ " LP: "+flex_LP)
            em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
        elif len(ranked_stats) == 1:
            if ranked_stats[0]['queueType'] == 'RANKED_FLEX_SR':
                flex_stats = ranked_stats[0]
                for each in flex_stats:
                    if each == 'tier':
                        flex_rank = flex_stats[each]
                    if each == 'rank':
                        flex_rank = flex_rank + ' ' + flex_stats[each]
                    if each == 'wins':
                        flex_wins = str(flex_stats[each])
                    if each == 'losses':
                        flex_losses = str(flex_stats[each])
                    if each == 'leaguePoints':
                        flex_LP = str(flex_stats[each])
                flex_ratio = str(int(int(flex_wins)/(int(flex_wins)+int(flex_losses)) * 100))
                em = discord.Embed(title=title_name, url = "https://www.op.gg/summoners/na/"+write_name, description= "Ranked Solo: UNRANKED, LP: 0"+
                "\nRanked Flex: "+ flex_rank + ', ' + flex_wins+"W/"+flex_losses+"L, Win Rate: "+flex_ratio+ " LP: "+flex_LP)
                em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
            if ranked_stats[0]['queueType'] == 'RANKED_SOLO_5x5':
                solo_stats = ranked_stats[0]
                for each in solo_stats:
                    if each == 'tier':
                        solo_rank = solo_stats[each]
                    if each == 'rank':
                        solo_rank = solo_rank + ' ' + solo_stats[each]
                    if each == 'wins':
                        solo_wins = str(solo_stats[each])
                    if each == 'losses':
                        solo_losses = str(solo_stats[each])
                    if each == 'leaguePoints':
                        solo_LP = str(solo_stats[each])
                solo_ratio = str(int(int(solo_wins)/(int(solo_wins)+int(solo_losses)) * 100))
                em = discord.Embed(title=title_name, url = "https://www.op.gg/summoners/na/"+write_name, description= "Ranked Solo: "+ solo_rank + ', ' + solo_wins+"W/"+solo_losses+"L, Win Rate: "+solo_ratio+ " LP: "+solo_LP+ "\nRanked Flex: UNRANKED, LP: 0")
                em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")
        else:
            em = discord.Embed(title=name, url = "https://www.op.gg/summoners/na/"+name, description= "Ranked Solo: UNRANKED, LP: 0" + "\nRanked Flex: UNRANKED, LP: 0")
            em.set_footer(text= "Created by bobapark, Sourced through op.gg + RiotAPI")

        await interaction.response.send_message(embed=em)
            
    bot.run(TOKEN)

