import os
import requests
import random
import string
import time
import discord
from flask import Flask

app = Flask(__name__)

# Function to generate a 19-digit code
def generate_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=19))
    return code

# Function to send request and check response code
def send_request_and_check():
    base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
    code = generate_code()
    url = f"{base_url}{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    if response.status_code == 200:
        discord_webhook_url = os.getenv("HOOKS")  # Retrieve webhook URL from environment variable
        discord_message = f"Generated code: {code}\nFull URL: {url}"
        send_discord_message(discord_webhook_url, discord_message)
    else:
        print("Request failed, trying again...")
        time.sleep(1)  # Adjust this delay as needed
        send_request_and_check()

# Function to send Discord message
def send_discord_message(webhook_url, message):
    webhook = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
    webhook.send(message)

# Route to display "I am alive"
@app.route('/')
def index():
    return "I am alive"

# Main loop
if __name__ == "__main__":
    # Run Flask app in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'host':'0.0.0.0','port':5000}).start()
    
    while True:
        send_request_and_check()
