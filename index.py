from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

discord_webhook_url = os.getenv("DISCORD_WEBHOOK", "EMPTY")
fc_code = os.getenv("FC_CODE")
fc_port = int(os.getenv("FC_PORT", "3000"))

if discord_webhook_url == "EMPTY":
    raise Exception("missing DISCORD_WEBHOOK env")

if fc_code is None:
    raise Exception("missing FC_CODE env")


def check_valid():
    returnResult = {"message": "no error", "success": True}

    if "code" not in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[code] is empty"

    if "userid" not in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[userid] is empty"

    if "name" not in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[name] is empty"

    if "message" not in request.form:
        returnResult["success"] = False
        returnResult["message"] = "[message] is empty"

    return returnResult


@app.route("/send_feedback", methods=["POST"])
def send_feedback():
    resultReturn = {"message": "something wrong", "success": False}

    if request.method == "POST":
        checkValid = check_valid()
        if checkValid["success"]:
            code = request.form["code"]
            playerUserId = request.form["userid"]
            playerName = request.form["name"]
            playerMessage = request.form["message"]

            if code == fc_code:
                webhook = DiscordWebhook(url=discord_webhook_url)
                embed = DiscordEmbed(
                    title="Feedback", description=playerMessage, color=5810431
                )
                embed.set_author(
                    name=playerName,
                    url=f"https://www.roblox.com/users/{playerUserId}/profile",
                    icon_url=f"https://www.roblox.com/headshot-thumbnail/image?userId={playerUserId}&width=420&height=420&format=png",
                )

                embed.set_footer(
                    text=f"sender is ruski boi from gip with client userid -> {playerUserId}"
                )
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()

                if response.ok:
                    resultReturn["message"] = "feedback sent to developer"
                    resultReturn["success"] = True

        else:
            resultReturn["message"] = checkValid["message"]

    return resultReturn


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=fc_port, debug=True)
