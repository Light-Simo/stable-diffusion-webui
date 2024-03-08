import requests


def send_message_to_slack(message="Hey slack, sending this straight from python"):
    # Define the URL of the Slack webhook
    webhook_url = "https://hooks.slack.com/services/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"

    # Define the payload in Python dictionary format
    payload = {
        "channel": "#automatic1111",
        "username": "webhookbot",
        "text": message,
        "icon_emoji": ":ghost:"
    }

    # Send the POST request to the Slack webhook
    response = requests.post(webhook_url, json=payload)

    # Check the response status code
    if response.status_code == 200:
        print("Message sent successfully!")
        print(response.text)
    else:
        print(f"Failed to send the message. Status code: {response.status_code}")
