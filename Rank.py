# Imports
from flask import Flask, request
from roblox import Client, RobloxException
import asyncio
from requests import post
from dotenv import load_dotenv
from os import getenv
# Variables
load_dotenv()
client = Client(getenv("ROBLOXTOKEN"))
# Functions
async def ShoutFunc(GroupID: int, Message: str):
    print(GroupID, Message)
    try:
        user = await client.get_authenticated_user()
        print("ID:", user.id)
        print("Name:", user.name)
        await client.get_base_group(GroupID).update_shout(Message)
        post(getenv("DISCORDWEBHOOK"), data=[("content", f"```fix\nShouting  '{str(Message)}'```")])
        return "Shouting.."
    except RobloxException as exception:
        post(getenv("DISCORDWEBHOOK"), data=[("content", "<@&955859397005938758> Something went wrong with the ranking bot! ```diff\n-" + str(exception) + "```")])
        return "Something went wrong while shouting..." + str(exception)
async def RankFunc(GroupID: int, UserID: int, RankID: int):
    print(GroupID, UserID, RankID)
    try:
        user = await client.get_authenticated_user()
        print("ID:", user.id)
        print("Name:", user.name)
        await client.get_base_group(GroupID).set_rank(UserID, RankID)
        user = await client.get_user(UserID)
        post(getenv("DISCORDWEBHOOK"), data=[("content", f"```fix\nRanking  {str(user.name)} to {str(RankID)}```")])
        return "Ranking.."
    except RobloxException as exception:
        post(getenv("DISCORDWEBHOOK"), data=[("content", "<@&955859397005938758> Something went wrong with the ranking bot! ```diff\n-" + str(exception) + "```")])
        return "Something went wrong while ranking..." + str(exception)
# Server
app = Flask(__name__)
@app.route('/')
def Home():
    print("Bot waking up.")
    return "Hi."
@app.route('/Rank')
def Rank():
    GroupID = request.args.get('GroupID')
    UserID = request.args.get('UserID')
    RankID = request.args.get('RankID')
    print(request.args)
    Status = asyncio.run(RankFunc(int(GroupID), int(UserID), int(RankID)))
    print(Status)
    return Status
@app.route('/Shout')
def Shout():
    GroupID = request.args.get('GroupID')
    Message = request.args.get('Message')
    print(request.args)
    Status = asyncio.run(ShoutFunc(int(GroupID), str(Message)))
    print(Status)    
    return Status
app.run()