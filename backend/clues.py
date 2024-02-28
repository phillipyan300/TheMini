from boardGenerator import run
import random
import json

FILEPATH = "./rawPrep/masterNYTList.txt"
#Now need to get the clues
def viewBoard(board):
    for row in board:
        print(row)

def viewClues(horizontal, vertical):
    # Since clue numbers start with human readable 1, not 0
    for i in range(1, len(horizontal)+1):
        print(f"{horizontal[i]:{70}}{vertical[i]}")

# difficulty parameter temporary, waiting on the master NYT list to finish parsing
def getInfo(difficulty: int):
    # Get the clues:
    with open(FILEPATH, 'r') as file:
        clues = json.load(file)

    # Get the generated board 
    board = run()
    viewBoard(board)

    horizHash = {}
    vertHash = {}
    # Get the horizontal clues
    counter = 1
    for row in board:
        word = "".join(row)
        options = clues[word]
        #Chooses a random clue from the clue bank
        randomClue = random.randint(0, len(options)-1)

        horizHash[counter] = options[randomClue]
        counter += 1
    
    # Get the vertical clues
    counter = 1
    for j in range(len(board[0])):
        # Utilize a string builder using a list
        word = []
        for i in range(len(board)):
            word.append(board[i][j])
        word = "".join(word)

        options = clues[word]

        #Chooses a random clue from the clue bank
        randomClue = random.randint(0, len(options)-1)

        vertHash[counter] = options[randomClue]
        counter += 1
    #print(board)
    viewClues(horizHash, vertHash)
    retDict = {}
    retDict["board"] = board
    retDict["horizontal"] =  horizHash
    retDict["vertical"] = vertHash
    
    return retDict




if __name__ == "__main__":
    #Set base difficulty to 4
    getInfo(4)