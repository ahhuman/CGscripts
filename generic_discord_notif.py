import sys
import requests

# Discord Webhook URL (replace with your actual webhook URL)
DISCORD_WEBHOOK_URL = "webhookurl"

def send_discord_message(file_name="Unknown file"):
    # Customizable message with file name
    discord_message = {
        "content": f" `{file_name}` has finished rendering"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)
        if response.status_code == 204:
            print("Discord notification sent successfully.")
        else:
            print(f"Failed to send Discord message: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error while sending Discord message: {e}")

if __name__ == "__main__":
    # Get the file name from the command line arguments
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "Houdini File"
    
    send_discord_message(file_name)
