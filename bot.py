#!/usr/bin/python3

import discord
import os
import yaml
from random import choice

def load_yaml(filename):
    with open(filename) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def draw_card(config, meanings):
    try:
        os.listdir(config['IMAGE_FOLDER'])
    except OSError:
        return "Please check your image folder config. Kismet can't read it."
    file_name = choice(os.listdir(config['IMAGE_FOLDER']))
    if not meanings:
        name = file_name.split('.')[0]
        if '_flipped' in name:
            name = "{} flipped".format(name.split('_')[0])
        embed = discord.Embed()
        embed.set_image(url="attachment://{}".format(file_name))
        embed.set_footer(text = name)
    else:
        if '_' in file_name:
            card_id = file_name.split('.')[0].split('_')[0]
        else:
            card_id = file_name.split('.')[0]
        meaning = meanings[int(card_id)]
        embed = '{} \nUpright Meaning: {}\nReversed Meaning: {}\n{}'.format(meaning['name'], meaning['upright'], meaning['reversed'], meaning['quote'])

    file_path = "{}/{}".format(config['IMAGE_FOLDER'], file_name)
    file = discord.File(file_path, filename=file_name)
    return (file, embed)

def main():
    config = load_yaml('config.yaml')
    try:
        meanings = load_yaml('meanings.yaml')
    except FileNotFoundError:
        meanings = False
    discordToken = config['DISCORD_TOKEN']
    command_name = config['COMMAND_NAME']
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("{} has connected to discord".format(client.user))
        for guild in client.guilds:
            print("Connected to: {}".format(guild))


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith(command_name):
            if "help" in message.content:
                response = "I'm your way to tempt fate. \n" \
                           "I can do the following for you:\n" \
                           "{} draw: Draw a card\n"\
                           "{}: Draws a card as well\n"\
                           "{} help: Show this help\n".format(command_name, command_name, command_name)
                await message.channel.send(response)
            elif message.content == command_name or message.content == "{} draw".format(command_name):
                card = draw_card(config, meanings)
                (image, embed) = card
                await message.channel.send(file=image, embed=embed)
            else:
                response = "Fate does not smile upon you, try again."
                await message.channel.send(response)

    client.run(discordToken)


if __name__ == '__main__':
    main()