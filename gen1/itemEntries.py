import os
import json

gamePath = "dexProjectDataminer/ThirdParty/gen1/pokered"

with open(gamePath + "/constants/item_constants.asm") as item_constants:
    item_id = 0
    items = {}
    item_constants_list = list(item_constants)
    for i in item_constants_list:
        if "FLOOR_B2F" in i:
            break
        elif i.startswith("\tconst "):
            item = i.split()[1]
            items[item_id] = item
            item_id += 1

    print(items)

    hms = {}
    hm_id = 1
    for i in item_constants_list:
        if i.startswith("\tadd_hm"):
            item = i.split()[1]
            hms[hm_id] = item
            hm_id += 1
    
    print(hms)
    
    tms = {}
    tm_id = 1
    
    for j in item_constants_list:
        if j.startswith("\tadd_tm "):
            item = j.split()[1]
            tms[tm_id] = item
            tm_id += 1
    
    print(tms)
    
with open(gamePath + "/data/items/key_items.asm") as key_items:
        keyItems = {}
        item_id = 1
        for i in key_items:
            if i.startswith("\tdbit "):
                value = i.split()[1]
                if value == "TRUE":
                    keyItems[item_id] = True
                else:
                    keyItems[item_id] = False
                item_id += 1
        print(keyItems)
        
with open(gamePath + "/data/items/names.asm") as item_names:
    names = {}
    item_id = 1
    for i in item_names:
        if i.startswith("\tli "): 
            names[item_id] = i.split('"')[1]
            item_id += 1            
        elif "assert_list_length NUM_ITEMS" in i:
            break
    print(names)
    
with open(gamePath + "/data/items/prices.asm") as item_prices:
    prices = {}
    item_id = 1
    for i in item_prices:
        if i.startswith('\tbcd3'):
            prices[item_id] = i.split()[1]
            item_id += 1
        elif "assert_table_length NUM_ITEMS" in i:
            break
    print(prices)
    
with open(gamePath + "/data/items/tm_prices.asm") as tm_prices:
    tmPrices = {}
    item_id = 1
    for i in tm_prices:
        if i.startswith("\tnybble "):
            tmPrices[item_id] = int(i.split()[1]) * 1000
            item_id += 1
    print(tmPrices)

hmsList = {}
for i in hms:
    hmsList[i] = {"move": hms[i]}
tmsList = {}
for i in tms:
    tmsList[i] = {"move":tms[i],"price": tmPrices[i]}

itemsList = {}
for i in items:
    if i != 0:
        itemsList[i] = {"item": items[i], "name": names[i], "price": prices[i], "isKeyItem": keyItems[i]}
        
with open("gen1/items.json", "w") as output:
    print(json.dumps(itemsList))
