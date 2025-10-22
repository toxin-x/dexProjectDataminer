import os 
import json
# TODO: evomoves



gamePath = "dexProjectDataminer/ThirdParty/gen1/pokered"

#get dex ids
with open(gamePath + "/constants/pokedex_constants.asm", "r") as dex_constants:
    dexConstants = {}
    dexNum = 1
    for i in dex_constants:
        if i.startswith("\tconst "):
            dexConstants[i.split(" ")[1]] = dexNum
            dexNum += 1

#get internal ids
with open(gamePath + "/data/pokemon/dex_order.asm", "r") as dex_order:
    dexOrder = {}
    currentID = 1
    for i in dex_order:
        if i.startswith("\tdb "):
            dexOrder[currentID] = i.split(" ")[1][:-1]
            currentID += 1


#evo moves
with open(gamePath + "/data/pokemon/evos_moves.asm", "r") as evo_moves:
    evoMovesList = list(evo_moves)
    evoMovesSplitList = []
    currentID = 1
    prevLine = 0
    for i, line in enumerate(evoMovesList):
        if line.endswith("EvosMoves:\n") or i == (len(evoMovesList) - 1):
                evoMovesSplitList.append(evoMovesList[prevLine:i-1])
                prevLine = i
    
    evoMoves = {}
    for i, mon in enumerate(evoMovesSplitList):
        evo = True
        evos = []
        moves = []
        line = ""

        for j in mon:
            if j.startswith("\tdb"):
                line = j.replace("\n", "").replace(",", "").split(" ")
                if line[1] == "0":
                    evo = False
                
                elif evo == True:
                    buildEvo = {"evo_method": line[1], "species": line[-1]}
                    if line[1] == "EVOLVE_LEVEL":
                        buildEvo["level"] = line[2]
                    elif line[1] == "EVOLVE_ITEM":
                        buildEvo["item"] = line[2]
                    elif line[1] == "EVOLVE_TRADE":
                        pass #every pokemon's evo trade minimum level is 1
                    evos.append(buildEvo)
                else:
                    moves.append({"level": line[1], "move": line[2]})
        evoMoves[i] = [evos, moves]
              
                
                 
            
    



#stats 
baseStats= {}
parentDir = gamePath + "/data/pokemon/base_stats/"
for baseStatFile in os.listdir(parentDir):
    with open(parentDir + baseStatFile, "r") as baseStatStream:
        BaseStat = list(baseStatStream)
        dbCount = 1
        tmhm = False
        tmhmLearnset = []
        for i in BaseStat:
            if i.startswith("\tdb" ):
                line = i.split()
                if dbCount == 1:
                    #current file's pokedex id
                    baseStats[dexConstants[line[1]]] = {}
                    currentEntry = baseStats[dexConstants[line[1]]]
                    
                    dbCount += 1
                    
                elif dbCount == 2:
                    #set stats
                    currentEntry["hp"] = line[1]
                    currentEntry["attack"] = line[2].strip(",")
                    currentEntry["defense"] = line[3].strip(",")
                    currentEntry["speed"] = line[4].strip(",")
                    currentEntry["special"] = line[5].strip(",")
                    
                    dbCount += 1
                    
                elif dbCount == 3:
                    #set type
                    currentEntry["type1"] = line[1].strip(",")
                    currentEntry["type2"] = line[2]
                    
                    dbCount += 1
                    
                elif dbCount == 4:
                    currentEntry["catchRate"] = int(line[1])
                    
                    dbCount += 1
                    
                elif dbCount == 5: 
                    currentEntry["baseExp"] = currentEntry["hp"] = line[1]
                    
                    dbCount += 1
                
                elif dbCount == 6:
                    lvl1Learnset = []
                    for move in line[1:5]:
                        lvl1Learnset.append(move.strip(","))
                    currentEntry["lvl1Learnset"] = lvl1Learnset
                    
                    dbCount += 1
                    
                elif dbCount == 7:
                    currentEntry["growthRate"] = line[1]
                    
                    dbCount += 1
            elif i.startswith("\ttmhm"):
                tmhm = True
                i = i.strip("\ttmhm")
            
            if tmhm:
                line = i.split()
                for move in line:
                    if "\\" not in move:
                        tmhmLearnset.append(move.strip(","))
                if "\\" not in i:
                    currentEntry["tmhmLearnset"] = tmhmLearnset
                    tmhm = False               

#make a dict of internal id to dex id
internalToDex = {}
for i in dexOrder:
    if dexOrder[i] != "":
        internalToDex[i] = dexConstants[dexOrder[i]]

#get names
with open(gamePath + "/data/pokemon/names.asm", "r") as pokemon_names:
    names = {}
    internalID = 1
    for i in pokemon_names:
        if i.startswith("\tdname "):
            names[internalID] = i.split('"')[1]
            internalID += 1

#get dex text
with open (gamePath + "/data/pokemon/dex_text.asm") as dex_text:
    dexText = {}
    currentText = ""
    fullText = ""
    for i in dex_text:
        if i.startswith("_"): 
            currentText = i[:-3]
            fullText = ""
        elif i == "\tdex\n":
            dexText[currentText] = fullText[:-1]
        elif i != "\n":
            fullText += i.split('"')[1] + " "
#open dex entries
with open(gamePath + "/data/pokemon/dex_entries.asm", "r") as dex_entries:
    dexEntries = list(dex_entries)
    preDex = {}
    internalID= 1
    for i, j in enumerate(dexEntries):
        #set internal ids 
        if "DexEntry\n" in j and "text_far" not in j:
            if "MissingNoDexEntry" not in j:
                preDex[j.split(" ")[1][:-1]] = {"internalID": internalID}
            internalID += 1
        
        #get dex entry
        if "DexEntry:" in j and j != "MissingNoDexEntry:\n":
            # 
            currentEntry = preDex[j[:-2]]
            
            
            
            
            # set species to be everything in quotes besides the last character (a @) on the line after the header
            currentEntry["species"] = dexEntries[i+1].split('"')[1][:-1]
            
            # get height to be everything after dw two lines after the header, then split it into feet and inches
            feet, inches = dexEntries[i+2].split(" ")[1][:-1].split(",")
            
            #set height in inches
            currentEntry["height"] = (int(feet) * 12) + int(inches)
            # set weight to be everything after dw three lines after the header
            currentEntry["weight"] = int(dexEntries[i+3].split(" ")[1][:-1])
             
            currentEntry["name"] = names[currentEntry["internalID"]]
            
            currentEntry["ID"] = internalToDex[currentEntry["internalID"]]
            
            currentEntry["text"] = dexText[dexEntries[i+4].split(" ")[1][:-1]]
            stats = baseStats[currentEntry["ID"]]
            
            for stat in stats:
                currentEntry[stat] = stats[stat]
            currentEntry["evolutions"], currentEntry["moves"] = evoMoves[currentEntry["internalID"]]

#resort dict by pokedex number instead of internal number
#yes i know this is stupid i am writing this while sick
dexNums = {}
for i in preDex:
    dexNums[preDex[i].pop("ID")] = preDex[i] 

dex = {}
i=1
while i < len(dexNums):
    dex[i] = dexNums[i]
    i += 1


with open ("gen1/pokered/pokemon.json", "w") as dump:
    json.dump(dex, dump)

