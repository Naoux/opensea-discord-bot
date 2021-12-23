What can the bot do ?
 - Display floor price instead of displaying current game.
![alt text](https://i.gyazo.com/8b58dbf31cab62fd4b4643c100cb40bd.png)

 - Send all new successful sales for a specific collection.
  ![alt text](https://i.gyazo.com/d3e37f5d67c7293f6ffe868f417ddec9.png)
  
 - Send all new listing for a specific collection.
 ![alt text](https://i.gyazo.com/92b403b3e80f068248d410726f6fee2e.png)
  
To make it work you need to:
  - clone the repo: `git clone https://github.com/Naoux/opensea-discord-bot.git`
  - install requirements: `pip install -r requirements.txt`
  - put OPENSEA_API_KEY, SALES_CHANNEL_ID, LISTINGS_CHANNEL_ID, DISCORD_TOKEN and COLLECTION_SLUG inside main.py
  - run it with `nohup python3 main.py &`

You can create a crontab task to run it at each reboot:
  - copy main.py into /bin: `cp main.py /bin/main.py`
  - open crontab and create the task: `crontab -e` and add this line `@reboot nohup python3 /bin/main.py &`
  - reboot your host and check with `ps ax` if the process is running.
