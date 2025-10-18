import os 

# TODO: evomoves, growthrates

#get dex ids
with open("dexProjectDataminer/ThirdParty/gen1/pokered/constants/pokedex_constants.asm", "r") as dex_constants:
    dexConstants = {}
    dexNum = 1
    for i in dex_constants:
        if i.startswith("\tconst "):
            dexConstants[i.split(" ")[1]] = dexNum
            dexNum += 1

#get internal ids
with open("dexProjectDataminer/ThirdParty/gen1/pokered/data/pokemon/dex_order.asm", "r") as dex_order:
    dexOrder = {}
    currentID = 1
    for i in dex_order:
        if i.startswith("\tdb "):
            dexOrder[currentID] = i.split(" ")[1][:-1]
            currentID += 1



#stats 
baseStats= {}
parentDir = "dexProjectDataminer/ThirdParty/gen1/pokered/data/pokemon/base_stats/"
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
                    currentEntry["atack"] = line[2].strip(",")
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
with open("dexProjectDataminer/ThirdParty/gen1/pokered/data/pokemon/names.asm", "r") as pokemon_names:
    names = {}
    internalID = 1
    for i in pokemon_names:
        if i.startswith("\tdname "):
            names[internalID] = i.split('"')[1]
            internalID += 1

#get dex text
with open ("dexProjectDataminer/ThirdParty/gen1/pokered/data/pokemon/dex_text.asm") as dex_text:
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
with open("dexProjectDataminer/ThirdParty/gen1/pokered/data/pokemon/dex_entries.asm", "r") as dex_entries:
    dexEntries = list(dex_entries)
    dex = {}
    internalID= 1
    for i, j in enumerate(dexEntries):
        #set internal ids 
        if "DexEntry\n" in j and "text_far" not in j:
            if "MissingNoDexEntry" not in j:
                dex[j.split(" ")[1][:-1]] = {"internalID": internalID}
            internalID += 1
        
        #get dex entry
        if "DexEntry:" in j and j != "MissingNoDexEntry:\n":
            # 
            currentEntry = dex[j[:-2]]
            
            
            
            
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
    print(dex)