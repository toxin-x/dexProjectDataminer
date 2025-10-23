import os
import json

gamePath = "dexProjectDataminer/ThirdParty/gen1/pokered"

with open(gamePath + "/constants/move_constants.asm") as move_constants:
    moves = {}
    moveID= 0
    for i in move_constants:
        if i.startswith("\tconst "):
            
            moves[i.split(" ")[1]] = moveID
            moveID +=1
        elif "DEF NUM_ATTACKS EQU const_value - 1" in i:
            break
    print(moves)

with open(gamePath + "/data/moves/names.asm") as move_names:
    moveNames = {}
    moveID = 1
    for i in move_names:
        if i.startswith("\tli "):
            moveNames[moveID] = i.split('"')[1]
            moveID+=1

with open(gamePath + "/data/moves/moves.asm") as move_table:
    moveData = {}
    moveID = 1
    for i in move_table:
        if i.startswith("\tmove "):
            move = i.strip().replace(",", "").split()
            moveData[moveID] = {"ID": move[1], "effect": move[2], "power": move[3], "type": move[4], "accuracy": move[5], "pp": move[6], "name": moveNames[moveID], }
            moveID += 1

with open("gen1/pokered/moves.json", "w") as file:
    json.dump(moveData, file) 