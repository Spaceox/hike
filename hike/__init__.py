import hikari
import tanjun
import os 

def initHikari() -> hikari.GatewayBot:
    bot = hikari.GatewayBot(os.environ.get("TOKEN"))
    initTanjun(bot)
    return bot

def initTanjun(bot: hikari.GatewayBot) -> tanjun.Client:
    if os.environ.get("DEV") != "":
        decGlobal = int(os.environ.get("DEVGUILD"))
    else:
        decGlobal = True
        
    client = tanjun.Client.from_gateway_bot(bot, declare_global_commands=decGlobal)
    
    client.load_modules("modules.__init__")
    return client