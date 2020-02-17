import random
import discord
import mpcalc

from discord.ext.commands import Bot

BOT_PREFIX = "cum!"
TOKEN = 'TOKEN'
MSG_SENT = False

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('Command does not exist.')

@client.command(pass_context=True)
async def cum(ctx):
    msg = 'poggers cum'
    await ctx.send(msg)

@client.command(pass_context=True)
async def roll(ctx):
    cums = random.randint(1, 100)
    cums = str(cums)
    response = 'you came ' + cums + ' times.'
    await ctx.send(response)

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title='Cum bot commands (prefix: cum!)',
        colour=discord.Color.blurple()
    )

    user = ctx.author
    embed.set_author(name='mmmm cum', icon_url=user.avatar_url)
    embed.set_footer(text='im footer')
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/619268946763186207.png?v=1')
    embed.add_field(name='not osu:', value='▸ **cum**, **noodle**, **roll**, **help (duh)**, **gay**, **store**', inline=False)
    embed.add_field(name='osu (note that these only work for tournament matches):', value='▸ **scores** (args: *link*): Lists the total score for each player within a match link and gives their cum rating.\n_ _\n'
                                                                                          '▸ **stats** (args: *link*, *player name*): Lists the maps played and scores of an individual player, as well as their total and average scores.\n_ _\n'
                                                                                          '▸ **map** (args: *link*, *keyword*): Given a keyword, searches for a map within the mp link and displays the scores for each player as well as the total and average score for that map. If teamvs enabled, shows total and averages for both teams.', inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    server_count = 0
    for guild in client.guilds:
        server_count += 1
    status = discord.Game('aw yeah baby im cumming on ' + str(server_count) + ' servers')
    await client.change_presence(activity=status)

@client.command(pass_context=True)
async def scores(ctx, link: str):
    player_ids = []
    players = []
    player_scores = []
    averages = []
    ratings = []
    all_maps = []
    individual_scores = []
    map_max_score = -1
    avg_top_scores = 0
    highest_rating_index = 0
    response = mpcalc.get_mp_data(link)
    pool_ids = mpcalc.get_mappool(response)

    for game in response['games']:
        if game['beatmap_id'] not in all_maps and game['beatmap_id'] in pool_ids:
            all_maps.append(game['beatmap_id'])
        for score in game['scores']:
            if score['user_id'] not in player_ids:
                player_ids.append(score['user_id'])
    for k in range(len(player_ids)):
        received_player = mpcalc.get_player_score(response, True, False, False, player_id=player_ids[k])
        individual_scores.append(mpcalc.get_player_score(response, False, True, False, player_id=player_ids[k]))
        player_scores.append(received_player)
        players.append(mpcalc.get_username(player_ids[k]))
        averages.append(int(received_player[players[k]]) / len(individual_scores[k]))
    for r in range(len(player_ids)):
        ratings.append(round(((averages[r]/1000000)*1.15)*((len(individual_scores[r])/(len(all_maps))))*2, 2))
    for x in range(len(ratings)):
        if ratings[x] > ratings[highest_rating_index]:
            highest_rating_index = x
    colon_index = mpcalc.get_colon_index(response)
    embed = discord.Embed(
        title=response['match']['name'][:colon_index],
        description = response['match']['name'][colon_index + 1:],
        colour = discord.Color.blue()
    )

    user = ctx.author
    embed.set_author(name='Match scores for '+response['match']['name'][:colon_index], icon_url=user.avatar_url)
    embed.set_footer(text='im footer')
    embed.set_thumbnail(url='https://a.ppy.sh/'+player_ids[highest_rating_index])
    for i in range(len(players)):
        embed.add_field(name=players[i], value='▸ **'+player_scores[i][players[i]]+'** ▸ Cum Rating 2.0.3: **'+str(ratings[i])+'**', inline=False)
    embed.add_field(name='Match history:', value=link)
    await ctx.send(embed=embed)

@scores.error
async def scores_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('No link found.')
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('Invalid link. (If argument is a match link and this shows up, pool is not in the database)')

@client.command(pass_context=True)
async def stats(ctx, link: str, player: str):
    userid = mpcalc.get_userid(player)
    response = mpcalc.get_mp_data(link)
    player = mpcalc.get_username(userid)
    scores = mpcalc.get_player_score(response, False, True, False, player_id=userid)
    map_ids = []
    map_names = []
    all_maps = []
    accuracies = []
    acc_sum = 0.0
    pool_ids = mpcalc.get_mappool(response)
    rating = 0

    for game in response['games']:
        if game['beatmap_id'] not in map_ids and game['beatmap_id'] in scores and game['beatmap_id'] in pool_ids:
            map_ids.append(game['beatmap_id'])
        if game['beatmap_id'] in pool_ids:
            if game['beatmap_id'] not in all_maps:
                all_maps.append(game['beatmap_id'])
        for score in game['scores']:
            if userid in score['user_id']:
                if game['beatmap_id'] in map_ids:
                    scores[game['beatmap_id']]['accuracy'] = round(((50*int(
                                                            scores[game['beatmap_id']]['50'])+100*int(
                                                            scores[game['beatmap_id']]['100'])+300*int(
                                                            scores[game['beatmap_id']]['300']))/(300*(int(
                                                            scores[game['beatmap_id']]['50'])+int(
                                                            scores[game['beatmap_id']]['100'])+int(
                                                            scores[game['beatmap_id']]['300'])+int(
                                                            scores[game['beatmap_id']]['miss']))))*100, 2)
    for id in map_ids:
        map_names.append(mpcalc.get_beatmaptitle(id))
        accuracies.append(scores[id]['accuracy'])
    colon_index = mpcalc.get_colon_index(response)
    total = int(mpcalc.get_player_score(response, True, False, False, player_id=userid)[player])
    average = total/(len(map_ids))
    for acc in accuracies:
        acc_sum += acc
    avg_acc = round((acc_sum) / (len(map_ids)), 2)

    rating = round(((average / 1000000) * 1.15) * ((len(map_ids) / (len(all_maps)))) * 2, 2)

    embed = discord.Embed(
        title=response['match']['name'][:colon_index],
        description=response['match']['name'][colon_index + 1:],
        colour=discord.Color.blue()
    )

    user = ctx.author
    embed.set_author(name='Player stats for ' + player, icon_url=user.avatar_url, url='https://osu.ppy.sh/u/'+userid)
    embed.set_footer(text='im footer')
    embed.set_thumbnail(url='https://a.ppy.sh/'+userid)
    for n in range(len(map_ids)):
        if scores[map_ids[n]]['mods'] != None:
            mod = ' **+'+mpcalc.Mod(int(scores[map_ids[n]]['mods'])).name+'**'
        else:
            mod = ''
        embed.add_field(name='Map '+str(n+1)+':', value='[**'+map_names[n]+'**](https://osu.ppy.sh/b/'+map_ids[n]+')'+mod+
                                                        '\n▸ **'+scores[map_ids[n]]['score']+'** ▸ '+str(scores[map_ids[n]]['accuracy'])+'%'+
                                                        '\n▸ **'+scores[map_ids[n]]['combo']+'x/'+mpcalc.get_map_data(map_ids[n])['max_combo']+'x** ▸ '+
                                                        scores[map_ids[n]]['300']+'/'+
                                                        scores[map_ids[n]]['100']+'/'+
                                                        scores[map_ids[n]]['50']+'/'+
                                                        scores[map_ids[n]]['miss'], inline=False)
    embed.add_field(name='_ _', value='Total score: **'+str(total)+'**\nAverage score: **'+str(int(average))+'**\nAverage accuracy: **'+str(avg_acc)+'%**\nCum rating 2.0.3: **'+str(rating)+'**', inline=False)
    embed.add_field(name='Match history:', value=link)
    await ctx.send(embed=embed)

@stats.error
async def stats_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('Please specify a link and/or a player in the match to calculate.')
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('Invalid link or player not found in mp link. (If argument is a match link and this shows up, pool is not in the database)')

@client.command(pass_context=True)
async def map(ctx, link: str, keyword: str):
    keywordl = keyword.lower()
    response = mpcalc.get_mp_data(link)
    player_ids = []
    players = []
    red = {}
    red_ids = []
    blue = {}
    blue_ids = []
    colon_index = mpcalc.get_colon_index(response)
    pool_ids = mpcalc.get_mappool(response)
    first_team = ''
    first_map = True
    change_first_map = False
    total = 0
    red_total = 0
    blue_total = 0
    difference = 0
    winner = ''
    red_printed = False
    blue_printed = False
    map_id = ''
    changed = False

    for game in response['games']:
        if game['beatmap_id'] in pool_ids and map_id == '':
            if keywordl in mpcalc.get_beatmaptitle(game['beatmap_id']).lower() or map_id == game['beatmap_id']:
                if first_map:
                    change_first_map = True
                for score in game['scores']:
                    if score['user_id'] not in player_ids:
                        player_ids.append(score['user_id'])
                        map_id = game['beatmap_id']
                        if game['team_type'] == '2':
                            if score['team'] == '2':
                                red[score['user_id']] = score['score']
                                red_ids.append(score['user_id'])
                                if first_map and first_team == '':
                                    first_team = score['team']
                            elif score['team'] == '1':
                                blue[score['user_id']] = score['score']
                                blue_ids.append(score['user_id'])
                                if first_map and first_team == '':
                                    first_team = score['team']
        if change_first_map:
            first_map = False
            change_first_map = False

    map_scores = (mpcalc.get_player_score(response, False, True, True, map=map_id))

    for game in response['games']:
        if game['beatmap_id'] == map_scores[player_ids[0]]['map']:
            for t in range(len(game['scores'])):
                if game['scores'][t]['user_id'] in player_ids:
                    map_scores[game['scores'][t]['user_id']]['accuracy'] = round(((50 * int(
                        map_scores[game['scores'][t]['user_id']]['50']) + 100 * int(
                        map_scores[game['scores'][t]['user_id']]['100']) + 300 * int(
                        map_scores[game['scores'][t]['user_id']]['300'])) / (300 * (int(
                        map_scores[game['scores'][t]['user_id']]['50']) + int(
                        map_scores[game['scores'][t]['user_id']]['100']) + int(
                        map_scores[game['scores'][t]['user_id']]['300']) + int(
                        map_scores[game['scores'][t]['user_id']]['miss'])))) * 100, 2)

    for v in range(len(player_ids)):
        total += int(map_scores[player_ids[v]]['score'])
    average = total / (len(map_scores))
    for x in range(len(blue_ids)):
        blue_total += int(blue[blue_ids[x]])
    for y in range(len(red_ids)):
        red_total += int(red[red_ids[y]])
    blue_average = blue_total / (len(map_scores)/2)
    red_average = red_total / (len(map_scores)/2)
    if blue_total > red_total:
        difference = blue_total - red_total
        winner = 'Blue team'
    elif red_total > blue_total:
        difference = red_total - blue_total
        winner = 'Red team'

    embed = discord.Embed(
        title=response['match']['name'][:colon_index],
        description=response['match']['name'][colon_index + 1:],
        colour=discord.Color.blue()
    )

    user = ctx.author
    embed.set_author(name='Map stats for ' + mpcalc.get_beatmaptitle(
        map_scores[player_ids[0]]['map']) + ' (keyword: ' + keyword + ')', icon_url=user.avatar_url)
    embed.set_footer(text='im footer')
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/619268946763186207.png?v=1')
    embed.set_image(url='https://assets.ppy.sh/beatmaps/' + mpcalc.get_map_data(map_scores[player_ids[0]]['map'])[
        'beatmapset_id'] + '/covers/cover.jpg')
    for z in range(len(player_ids)):
        players.append(mpcalc.get_username(player_ids[z]))
    if len(player_ids) % 2 == 1:
        player_ids.append('')
        players.append('')
        changed = True

    for c in range(int(len(player_ids) / 2)):
        if c == int(len(player_ids) / 2) - 1 and changed:
            value_str = '\u200b'
        else:
            if map_scores[player_ids[c + int(len(player_ids) / 2)]]['mods'] != None:
                mod2 = ' **+' + mpcalc.Mod(
                    int(map_scores[player_ids[c + int(len(player_ids) / 2)]]['mods'])).name + '**'
            else:
                mod2 = ''
            value_str = '[**' + players[c + int(len(player_ids) / 2)] + '**](' + 'https://osu.ppy.sh/u/' + \
                        player_ids[c + int(len(player_ids) / 2)] + ')\n▸ **' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['score'] + '** ▸ ' + str(
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['accuracy']) + '%' + '\n▸ **' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['combo'] + 'x/' + \
                        mpcalc.get_map_data(map_scores[player_ids[0]]['map'])['max_combo'] + 'x** ▸ ' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['300'] + '/' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['100'] + '/' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['50'] + '/' + \
                        map_scores[player_ids[c + int(len(player_ids) / 2)]]['miss'] + ' ' + mod2
        if map_scores[player_ids[c]]['mods'] != None:
            mod = ' **+' + mpcalc.Mod(int(map_scores[player_ids[c]]['mods'])).name + '**'
        else:
            mod = ''
        embed.add_field(name='\u200b',
                        value='[**' + players[c] + '**](' + 'https://osu.ppy.sh/u/' + player_ids[c] + ')\n▸ **' +
                        map_scores[player_ids[c]]['score'] + '** ▸ ' + str(
                        map_scores[player_ids[c]]['accuracy']) + '%' + '\n▸ **' +
                        map_scores[player_ids[c]]['combo'] + 'x/' + mpcalc.get_map_data(
                        map_scores[player_ids[0]]['map'])['max_combo'] + 'x** ▸ ' +
                        map_scores[player_ids[c]]['300'] + '/' +
                        map_scores[player_ids[c]]['100'] + '/' +
                        map_scores[player_ids[c]]['50'] + '/' +
                        map_scores[player_ids[c]]['miss'] + ' ' + mod, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='\u200b', value=value_str, inline=True)
    if response['games'][2]['team_type'] == '2':
        for n in range(0, 2):
            if blue_printed or first_team == '2' and n == 0:
                embed.add_field(name='\u200b', value='Red team average: **'+str(int(red_average))+'**', inline=True)
                if n == 0:
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    red_printed = True
            elif red_printed or first_team == '1' and n == 0:
                embed.add_field(name='\u200b', value='Blue team average: **' + str(int(blue_average)) + '**', inline=True)
                if n == 0:
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    blue_printed = True
        red_printed = False
        blue_printed = False
        for o in range(0, 2):
            if first_team == '2' and o == 0 or blue_printed == True:
                embed.add_field(name='\u200b', value='Red team total: **' + str(red_total)+'**', inline=True)
                if o == 0:
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    red_printed = True
            elif first_team == '1' and o == 0 or red_printed == True:
                embed.add_field(name='\u200b', value='Blue team total: **' + str(blue_total)+'**', inline=True)
                if o == 0:
                    embed.add_field(name='\u200b', value='\u200b', inline=True)
                    blue_printed = True
        embed.add_field(name='\u200b', value='Difference: **' + str(difference) + '**', inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        embed.add_field(name='\u200b', value='Winner: **' + winner + '**', inline=True)
    embed.add_field(name='\u200b',
                    value='Average score: **' + str(int(average)) + '**\n[Match history](' + link + ')',
                    inline=True)
    embed.add_field(name='\u200b', value='Total score: **' + str(total) + '**\n' + '[Beatmap link](' + 'https://osu.ppy.sh/b/' + map_id + ')', inline=True)
    await ctx.send(embed=embed)

@map.error
async def map_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('No keyword or link found (type something after link to search for map)')
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send('Invalid link or beatmap not found in mp link. (If argument is a match link and this shows up, pool is not in the database)')


@client.command(pass_context=True)
async def noodle(ctx):
    images = [
        discord.File('noodle.jpeg', filename='noodle.jpeg'),
        discord.File('noodle2.png', filename='noodle.png'),
        discord.File('noodle3.png', filename='noodle.png'),
        discord.File('narwhal.jpg', filename='noodle.jpg'),
    ]

    await ctx.send('',  file=random.choice(images))

@client.command(pass_context=True)
async def gay(ctx):
    image = discord.File('gay.jpg', filename='gay.jpg')

    await ctx.send('', file=image)

@client.command(pass_context=True)
async def store(ctx):
    user = ctx.author
    embed = discord.Embed(
        description= '<@'+str(user.id)+'> is driving to the cum store',
        colour=discord.Color.blurple()
    )

    #embed.set_footer(text='im footer')
    embed.set_image(url='https://media.discordapp.net/attachments/617001685415624704/659152275662700573/image0_1.gif')
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def chalice(ctx):
    user = ctx.author
    embed = discord.Embed(
        description= '<@'+str(user.id)+'> consumes the cum chalice',
        colour=discord.Color.blurple()
    )

    #embed.set_footer(text='im footer')
    embed.set_image(url='https://media1.tenor.com/images/2cca8e7beec7e9d09507bf85d65f8c04/tenor.gif')
    await ctx.send(embed=embed)

'''
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print('Current servers:')
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(6)

client.loop.create_task(list_servers())
'''
client.run(TOKEN)