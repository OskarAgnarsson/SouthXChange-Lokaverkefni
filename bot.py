import Southxchange
import json
import time

key = "YourKeyHere"
secret = "YourSecretKeyHere"

Southxchange.Southxchange(key,secret)#Need to put your own keys here

Wallets = Southxchange.Wallets()
Markets = Southxchange.Markets()
Market = Southxchange.Market()

def checkbalance():
    balances = json.loads(Wallets.balances())
    smlybalance = 0
    for i in balances:
        if i["Currency"] == "SMLY":#Finds SMLY wallet
            smlybalance = i["Available"]#Sets SMLY balance
    if smlybalance >= 2000:#Checks if I can afford to buy more LTC
        return True
    else:
        return False

def checkmarket():
    currenttime = time.time()*1000#Gets current time in milliseconds
    history = Markets.history("smly","ltc",int(currenttime-(3600*6*1000)),int(currenttime),2)#Gets history of last 6 hours
    if history[0]["PriceHigh"] < history[-1]["PriceHigh"]:#Checks the highest price in the most recent and the least recent time periods
        return True
    else:
        return False

log = "log.txt"

while True:
    if checkbalance() and checkmarket():#Checks if I have enough SMLY and if the market rate has improved
        smlyToLtcRate = Markets.price('smly','ltc')#Gets current rate
        Market.placeorder("SMLY", "LTC",amount=1000,type="SELL",limitprice=smlyToLtcRate["Bid"])#Places order to sell 1000 SMLY for LTC
        ctime = time.ctime()
        with open(log,"a") as f:
            f.write(ctime+": Bought "+str(smlyToLtcRate["Bid"]*1000)+" LTC\n")#Writes to log
    time.sleep(3600)#Waits an hour