import os
import json

gamePath = "dexProjectDataminer/ThirdParty/gen1/pokered"

with open(gamePath + "/data/events/trades.asm") as pokemon_trades:
    trades = []
    for i in pokemon_trades: 
        if i.startswith("\tnpctrade "):
            line = i.replace("  "," ").replace(",", "").split()
            trades.append({"give": line[1], "get": line[2], "nickname": line[4]})
    print(trades)
with open("gen1/pokered/trades.json", "w") as outfile:
    json.dump(trades, outfile)