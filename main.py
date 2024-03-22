import random
import string
import threading
import requests
from flask import Flask, request

app = Flask(__name__)

# Global variables to keep track of generated code count
generated_code_count = 0

# Placeholder URLs
fargate_gift_url = "https://discordapp.com/api/entitlements/gift-codes/"
placeholder_post_url = "https://ntfy.sh/easondiscord"
placeholder_start_url = "https://ntfy.sh/easondiscord"

def generate_code():
    """Generate a 24-character code with uppercase letters, lowercase letters, and numbers."""
    global generated_code_count
    generated_code_count += 1
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(24))

def send_requests(code):
    """Send GET and POST requests."""
    # Send GET request
    get_url = f"{fargate_gift_url}{code}"
    response = requests.get(get_url)
    if response.status_code == 200:
        # Send POST request if response code is 200
        requests.post(placeholder_post_url, data={'code': code})

def start_app():
    """Start the Flask web app and send a POST request."""
    global generated_code_count
    requests.post(placeholder_start_url, data={'message': 'App Started And Alive'})  # Sending POST request when the app starts
    app.run()

@app.route('/')
def index():
    """Display a message on the Flask website."""
    return 'App Started And Alive'

def send_notification():
    """Send a POST request with the count of generated codes."""
    global generated_code_count
    requests.post(placeholder_post_url, data={'code_count': generated_code_count})
    generated_code_count = 0  # Reset the count for the next 10 minutes
    threading.Timer(1800, send_notification).start()  # Schedule the next notification after 10 minutes

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_app)
    flask_thread.start()

    # Start sending notifications every 10 minutes
    send_notification()

    # Generate and send requests
    while True:
        code = generate_code()
        code_thread = threading.Thread(target=send_requests, args=(code,))
        code_thread.start()
