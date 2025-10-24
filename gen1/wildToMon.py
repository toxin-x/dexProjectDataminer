import os
import json

gamePath = "dexProjectDataminer/ThirdParty/gen1/pokered"

with open(gamePath + "/data/wild/probabilities.asm") as pokemon_probabilities:
    probabilities_bytes = []
    count = 0
    for i in pokemon_probabilities:
        if i.startswith("\tdb "):
            value = i.replace(",", "").replace("  ", " ").split(" ")[1]
            probabilities_bytes.append( int(value))
            count += 1
    
    probabilities_bytes.reverse()
    probabilities = []
     
    for i, prob in enumerate(probabilities_bytes):
        if i < len(probabilities_bytes) - 1:
            probabilities.append(prob - probabilities_bytes[i+1])
        else:  
            probabilities.append(prob + 1)            
    probabilities.reverse()
    print(probabilities)
    
parentDir = gamePath + "/data/wild/maps/"
maps = {}
for mapFile in os.listdir(parentDir):

    with open(parentDir + mapFile, "r") as mapStream:
        mapData = {"grass": [], "water": []}
        
        terrain = ""
        game = ["red", "blue"]
        count = 0
        subcount = 0
        for i in mapStream:
            if i.startswith("\tdb "):
                db = i.replace(",", "").replace("  ", " ").strip().split(" ")
                if len(game) == 1:
                    subcount += 1
                else: 
                    count += 1
                mapData[terrain].append({"pokemon": db[2], "level": int(db[1]), "rarity": count + subcount, "games": game})
            elif i.startswith("IF DEF(_RED)"):
                subcount = 0
                game = ["red"]
            elif i.startswith("IF DEF(_BLUE)"):
                subcount = 0
                game = ["blue"]
            elif i.startswith("ENDC"):
                game = ["red", "blue"]
            elif i.startswith("\tdef_grass_wildmons "):
                terrain = "grass"
                count = 0
                subcount = 0
            elif i.startswith("\tend_grass_wildmons"):
                terrain = ""
            elif i.startswith("\tdef_water_wildmons "):
                terrain = "water"
                count = 0
                subcount = 0
            elif i.startswith("\tend_water_wildmons"):
                terrain = ""
        maps[mapFile[:-4]] = mapData
with open("gen1/pokered/wildPokemon.json", "w") as file:
    json.dump(maps, file)
                