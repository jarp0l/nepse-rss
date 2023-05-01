# NEPSE-RSS

[![Convert SQLite db to RSS, deploy and notify](https://github.com/jarp0l/nepse-rss/actions/workflows/convert-deploy.yml/badge.svg)](https://github.com/jarp0l/nepse-rss/actions/workflows/convert-deploy.yml)

The project [sidbelbase/nepstonks](https://github.com/sidbelbase/nepstonks) scrapes the latest upcoming issues, news, and investment opportunities and sends them to a telegram channel. The scraped data is stored in SQLite database in the repo. 

But this project [jarp0l/nepse-rss](https://github.comjarp0l/nepse-rss) uses that database and converts those data into RSS feeds. The feeds are served using GitHub Pages:
- Stocks feed: https://jarp0l.github.io/nepse-rss/stocks.xml - feed of stock additions/new stocks
- Announcements feed: https://jarp0l.github.io/nepse-rss/announcements.xml - feed of announcements like allotments

These feeds are synced daily with the [sidbelbase/nepstonks](https://github.com/sidbelbase/nepstonks) project using GitHub Actions.

We use [MonitoRSS](https://monitorss.xyz/) bot in Discord to check the feeds regularly. Additionally, a reminder is sent to Discord if any stock has an opening/closing date that matches the day [the GitHub Actions workflow](.github/workflows/convert-deploy.yml) runs.
