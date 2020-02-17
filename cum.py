#https://discordapp.com/api/oauth2/authorize?client_id=655566467579772938&permissions=271969360&scope=bot

import discord
import random

TOKEN = 'NjU1NTY2NDY3NTc5NzcyOTM4.XfZ58g.YxjTsgSFxXP56g8TKNsrUALI51s'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('will you cum on'):
        possible_responses = [
            'yeah sure',
            'Perhaps.',
            'Absolutely not.',
            'HELL YEAAAA AOIJIOJVADOVIAS'
        ]
        await message.channel.send(random.choice(possible_responses))
    if message.content.startswith('hello cum bot'):
        await message.channel.send('die stinky bithc')
    if message.content.startswith('congrats!\nyou did it!'):
        await message.channel.send('congrats!\nyou did it!')
    if message.content.startswith('good morning cum bot'):
        possible_responses = [
            'Good morning dumbas s',
            'Shut up i hate yuo.',
        ]
        await message.channel.send(random.choice(possible_responses))
    if message.content.startswith('you live in this country') or message.content.startswith('i live in this country'):
        user = message.author
        embed = discord.Embed(
            description='<@' + str(user.id) + '> lives in this country',
            colour=discord.Color.blurple()
        )
        # embed.set_footer(text='im footer')
        embed.set_image(
            url='https://pbs.twimg.com/media/EN-xIqMXsAEzWrf?format=jpg&name=900x900')
        await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)