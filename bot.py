#!/usr/bin/python3

import discord
import os
import yaml
from random import choice

def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def draw_card(config):
    try:
        os.listdir(config['IMAGE_FOLDER'])
    except OSError:
        return "Please check your image folder config. Kismet can't read it."
    file_name = choice(os.listdir(config['IMAGE_FOLDER']))
    name = file_name.split('.')[0]
    if '_flipped' in name:
        name = "{} flipped".format(name.split('_')[0])
    file_path = "{}/{}".format(config['IMAGE_FOLDER'], file_name)
    file = discord.File(file_path, filename=file_name)
    embed = discord.Embed()
    embed.set_image(url="attachment://{}".format(file_name))
    embed.set_footer(text = name)
    return (file, embed)

def main():
    config = load_config()
    discordToken = config['DISCORD_TOKEN']
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
        if message.content.startswith("!kismet"):
            if "help" in message.content:
                response = "I'm your way to tempt fate. \n" \
                           "I can do the following for you:\n" \
                           "!kismet draw: Draw a card\n" \
                           "!kismet: Draws a card as well\n" \
                           "!kismet help: Show this help\n"
                await message.channel.send(response)
            elif message.content == "!kismet" or message.content == "!kismet draw":
                card = draw_card(config)
                (image, embed) = card
                await message.channel.send(file=image, embed=embed)
            else:
                response = "Fate does not smile upon you, try again."
                await message.channel.send(response)

    client.run(discordToken)


if __name__ == '__main__':
    main()