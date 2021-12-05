from logging import lastResort
from discord.ext import commands, tasks
import datetime, random, requests, discord

API_KEY = ""
DISCORD_CHANNEL_ID = 
DISCORD_TOKEN = ""
COLLECTION_SLUG = "soulware-origins"

intents         = discord.Intents.default()
intents.members = True
bot             = commands.Bot(command_prefix="!", intents=intents)
lastSalesNumber = 0
headers         = {
    "Accept": "application/json",
    "X-API-KEY": API_KEY
}
bot.remove_command("help")

@tasks.loop(minutes=1)
async def getFloorPrice():
    url        = "https://api.opensea.io/api/v1/collection/{}/stats".format(COLLECTION_SLUG)
    response   = requests.request("GET", url, headers=headers).json()
    floorPrice = response['stats']['floor_price']
    
    await bot.change_presence(activity=discord.Game(name='Floor price: {}eth'.format(floorPrice)))

@tasks.loop(minutes=1)
async def getSales():
    global lastSalesNumber
    url      = "https://api.opensea.io/api/v1/events"
    now      = datetime.datetime.now() - datetime.timedelta(seconds=120)
    date     = now.strftime("%Y-%m-%dT%H:%M:%S+01:00")
    params   = {
        'collection_slug': COLLECTION_SLUG,
        'event_type':      'successful',
        'only_opensea':    'false',
        'offset':          0,
        'limit':           300,
        'occurred_after':  date
    }
    try:
        response = requests.request("GET", url, headers=headers, params=params).json()
    except:
        pass
    try:
        if len(response['asset_events']):    
            count = 0
            for sales in response['asset_events'][::-1]:
                salesData = {}
                try:
                    salesData['nftId']        = sales['asset']['name']
                    salesData['animationUrl'] = sales['asset']['animation_url']
                    salesData['imageUrl']     = sales['asset']['image_original_url']
                    salesData['when']         = " ".join(sales['transaction']['timestamp'].split("T")).replace("-", "/")
                    salesData['txUrl']        = 'https://etherscan.io/tx/{}'.format(sales['transaction']['transaction_hash'])
                    salesData['symbol']       = sales['payment_token']['symbol']
                    salesData['eth_price']    = "{}{}".format(round(float(sales['total_price']) / float(10**18), 2), salesData['symbol'])
                    salesData['usd_price']    ="${}".format(",".join([str(round(float(sales['total_price']) / float(10**18) * float(sales['payment_token']['usd_price'])))[::-1][i:i+3] for i in range(0, len(str(round(float(sales['total_price']) / float(10**18) * float(sales['payment_token']['usd_price'])))), 3)])[::-1])

                    try:    
                        salesData['seller'] = sales['seller']['user']['username']
                        if salesData['seller'] == None:
                            salesData['seller'] = sales['seller']['address'][0:8]
                    except:
                        salesData['seller'] = sales['seller']['address'][0:8]
                    try:
                        salesData['buyer'] = sales['winner_account']['user']['username']
                        if salesData['buyer'] == None:
                            salesData['buyer'] = sales['winner_account']['address'][0:8]
                    except:
                        salesData['buyer'] = sales['winner_account']['address'][0:8]

                    try:
                        messages = await bot.get_channel(DISCORD_CHANNEL_ID).history(limit=lastSalesNumber).flatten() 
                        same    = 0
                        i        = 0
                        while same == 0:
                            msg = messages[i]
                            if salesData["txUrl"] == msg.embeds[0].url:
                                same += 1   
                            i += 1
                        if same:
                            continue
                    except:
                        pass
                    if salesData['seller'] != "Soulware-Deployer":
                        embed = discord.Embed(title="{} Sold !".format(salesData['nftId']), description="New OG ?", url=salesData['txUrl'], color=discord.Colour.random())
                        embed.set_author(name="SLWR Market", icon_url="https://www.soulwareproject.com/images/about.png", url="https://www.soulwareproject.com/")
                        embed.add_field(name="Seller", value=salesData['seller'], inline=True)
                        embed.add_field(name="Buyer", value =salesData['buyer'], inline=True)
                        embed.add_field(name="When", value =salesData['when'], inline=True)
                        embed.add_field(name="Price", value ="{} / {}".format(salesData['eth_price'], salesData['usd_price']), inline=False)
                        embed.set_image(url=salesData['imageUrl'])
                        embed.set_footer(text="Powered by #Soulwarriors")
                        await bot.get_channel(DISCORD_CHANNEL_ID).send(embed=embed)
                        count += 1
                except:
                    pass
            lastSalesNumber = count  
    except:
        pass  
    
@getSales.before_loop
async def before():
    await bot.wait_until_ready()

@getFloorPrice.before_loop
async def before():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    print("Bot is ready !")
    getFloorPrice.start()
    getSales.start()

bot.run(DISCORD_TOKEN)
