import openai
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
discord_token = os.getenv("discord_token")
gpt_token = os.getenv("openAi_key") 

openai.api_key = gpt_token

intents = discord.Intents().all()
intents.message_content = True
intents.guilds = True
intents.members = True


bot = commands.Bot(command_prefix="/", intents = intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is launched !")


@bot.command(name = "askMc")  #ask Micro Club *_*
async def ask(ctx, *, question):
    #Sending the msg of the user to the API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=100   #max lenghth of response
    )

    # Sending the response to the user
    await ctx.send(response.choices[0].text.strip())


@bot.command(name = "drawMc")  
async def draw(ctx, *, cmd):
    #getting the name of the user (writer of the command)
    username = ctx.author.display_name   
    #this msg will be displayed while the image is not generated yet
    waiting_msg = await ctx.send(f"Please wait... dear {username}")
    #Sending the msg to the API
    response = openai.Image.create(
    prompt=cmd,
    n=1,
    size="256x256",
    )
    #replacing the waiting msg by the generated image
    await waiting_msg.edit(content =response["data"][0]["url"] )

    

bot.run(discord_token)

