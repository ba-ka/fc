from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, redirect, url_for, request
import os

app = Flask(__name__)

def check_valid():
    returnResult = {
        "message": "no error",
        "success": True
    }

    if not 'code' in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[code] is empty"
    
    if not 'userid' in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[userid] is empty"
    
    if not 'name' in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[name] is empty"
    
    if not 'message' in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[message] is empty"

    return returnResult

@app.route('/send_feedback',methods = ['POST'])
def send_feedback():
    resultReturn = {
        "message": "something wrong",
        "success": False
    }

    if request.method == 'POST':
        checkValid = check_valid()
        if checkValid["success"]:
            code = request.form['code']
            playerUserId = request.form['userid']
            playerName = request.form['name']
            playerMessage = request.form['message']

            if code == os.getenv('FC_CODE'):
                webhook = DiscordWebhook(url=os.getenv('DISCORD_WEBHOOK'))
                embed = DiscordEmbed(
                    title = "Feedback", description = playerMessage, color = 5810431
                )
                embed.set_author(
                    name= playerName,
                    url= f"https://www.roblox.com/users/{ playerUserId }/profile",
                    icon_url= f"https://www.roblox.com/headshot-thumbnail/image?userId={ playerUserId }&width=420&height=420&format=png",
                )

                embed.set_footer(text=f"sender is ruski boi from gip with client userid -> { playerUserId }")
                embed.set_timestamp()

                webhook.add_embed(embed)
                
                response = webhook.execute()
                resultReturn["message"] = "feedback sent to developer"
                resultReturn["success"] = True

        else:
            resultReturn["message"] = checkValid["message"]
    
    return resultReturn
