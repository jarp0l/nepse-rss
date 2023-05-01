import json
import string
import sys
from datetime import date
from os import environ

import requests
from dotenv import find_dotenv, load_dotenv
from requests.exceptions import HTTPError

load_dotenv(find_dotenv())
WEBHOOK_URL = environ["WEBHOOK_URL"]


def prepare_payload(data, **kwargs) -> dict:
    open_or_close = kwargs["status"]
    date_today = kwargs["today"]

    embed_template = string.Template(
        """
          {
            "content": "<@&1102291384515444926>",
            "embeds": [
              {
                "title": "Reminder :warning:",
                "description": "**${company}** ${open_or_close} today (${date_today})!",
                "color": 16199936,
                "footer": {
                  "text": "Synced: ${sync_timestamp}"
                }
              }
            ],
            "username": "Stocks Reminder",
            "avatar_url": "https://imgur.com/a/9VGkPGn"
          }
      """
    )

    payload = embed_template.substitute(
        company=data["company_name"],
        open_or_close=open_or_close,
        date_today=date_today,
        sync_timestamp=data["stock_added_at"],
    )

    return json.loads(payload)


def notify_discord(payload):
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except HTTPError as exc:
        status_code = exc.response.status_code
        print(f"Error! {status_code}")
        exit(code=status_code)


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    status = ""
    payload = ""
    today = date.today().strftime("%Y-%m-%d")

    for item in data:
        if item["opening_date"] == today:
            status = "opens"
        if item["closing_date"] == today:
            status = "closes"

        if status:
            payload = prepare_payload(item, today=today, status=status)
            notify_discord(payload)
