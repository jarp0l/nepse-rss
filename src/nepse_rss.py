import argparse
import json
import re
import sys
from datetime import datetime

from feedgen.feed import FeedGenerator

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--stock",
    action="store_true",
    help="Create RSS feed for 'stock' table",
)
parser.add_argument(
    "-a",
    "--announcement",
    action="store_true",
    help="Create RSS feed for 'announcement' table",
)
args = parser.parse_args()


# Read JSON input from stdin
data = json.load(sys.stdin)

# Create RSS feed
fg = FeedGenerator()
fg.link(href="https://www.nepalstock.com.np/")

# Add items to RSS feed
for item in data:
    fe = fg.add_entry()
    if args.stock:
        # Feed title
        fg.title("Stocks feed")
        fg.description("RSS feed of recent stocks")

        fe.title(item["company_name"])
        fe.link(href=item["pdf_url"])
        fe.description(
            f"""
            Company: {item["scrip"]} - {item["company_name"]}<br>
            Stock type: {item["stock_type"]}<br>
            Opens on: {item["opening_date"]}<br>
            Closes on: {item["closing_date"]}<br>
            Units: {item["units"]}<br>
            Issued by: {item["issued_by"]}
            """
        )
        # Convert date string to datetime object
        date_obj = datetime.strptime(
            item["stock_added_at"], "%Y-%m-%d %H:%M:%S.%f"
        )

        # Format datetime object as ISO 8601 date format
        rss_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        fe.published(rss_date)

    elif args.announcement:
        # Feed title
        fg.title("Announcements feed")
        fg.description("RSS feed of recent announcements")

        pattern = r"^(.*\ballotted\b).*"
        match = re.match(pattern, item["content"])
        if match:
            truncated = match.group(1) + "..."
            fe.title(truncated)

        fe.link(href=item["content_url"])
        fe.description(
            f"""
            {item["content"]}
            <br><br>
            Published on: {item["published_date"]}
            """
        )
        # Convert date string to datetime object
        date_obj = datetime.strptime(item["scraped_at"], "%Y-%m-%d %H:%M:%S.%f")

        # Format datetime object as ISO 8601 date format
        rss_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
        fe.published(rss_date)

# Output RSS feed to stdout
sys.stdout.write(fg.rss_str(pretty=True).decode())
