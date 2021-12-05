What can the bot do ?
 - Display floor price instead of displaying current game.
![alt text](https://i.gyazo.com/8b58dbf31cab62fd4b4643c100cb40bd.png)

 - Send all new successful sales for Soulware Origins (Genesis).
  ![alt text](https://i.gyazo.com/7d8d7cb51940511c100540151778afc8.png)
  
To make it work you need to:
  - clone the repo: `git clone https://github.com/Naoux/soulwareSalesBot/`
  - install requirements: `pip install -r requirements.txt`
  - put OPENSEA_API_KEY, DISCORD_CHANNEL_ID, DISCORD_TOKEN and COLLECTION_SLUG inside main.py
  - run it with `nohup python3 main.py &`

You can create a crontab task to run it at each reboot:
  - copy main.py into /bin: `cp main.py /bin/main.py`
  - open crontab and create the task: `crontab -e` and add this line `@reboot nohup python3 /bin/main.py &`
  - reboot your host and check with `ps ax` if the process is running.
