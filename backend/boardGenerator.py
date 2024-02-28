import random
import json
import sys
from collections import deque
import re
import copy

# Dimensions must be greater than or equal to 1, otherwise will have unexpected bugs
DIMENSION = 5
FILEPATH = "./rawPrep/masterNYTList.txt"

def getWords(filePath):

    # Open the file and load its contents into a Python dictionary
    with open(filePath, 'r') as file:
        data = json.load(file)
    #print(data)

    return data

def initialSeed(board, WORDLIST) -> list:
    # Start by randomly seeding the first row
    randomStart = chooseRandom(list(WORDLIST.keys()))

    # Set seed for testing purposes
    #randomStart = "ENIAC"

    #For each of the columns
    for i in range(len(board[0])):
        board[0][i] = randomStart[i]
     
    return [board, randomStart]


def findBestOption(board, horizontal, wordBag: list, container, WORDLIST):
    #print("Find Best Option")
    maxScore = [0, " ", " ", " "]

    #First we need to make sure the wordBag isn't too big. 
    if len(wordBag) > 5:
        wordBag = random.sample(wordBag, 5)

        
    #TODO Need to remove words from wordbag which have failed. not needed, just optimization
    elif len(wordBag) == 0:
        return ["BACKTRACK", " ", " "]


    #Find which container has the smallest score, and move onto that one with the new wordbag and container
    for word in wordBag:
        #Temporarily change the board to reflect this potential word
        tempBoard = updateBoard(board, word, container)
        #print(f"The state of the temporary board")
        #viewBoard(tempBoard)

        # if the board is full, you need to check if it is satisfied
        if checkBoardFull(tempBoard):
            finished = checkFullBoardCorrect(board, WORDLIST)
            if finished:
                return [tempBoard, "FINISHED", " "]
            else:
                #Otherwise, this is not the right word
                continue
        


        [score, potentialWordBag, potentialNextContainer] = scoreAlgorithm(tempBoard, horizontal, container, WORDLIST)
        #print(f"The score for this is: {score} with bag: {potentialWordBag}")

        # If there are no options intersecting this word. Skip
        if score == sys.maxsize:
            continue

        if score >= maxScore[0]:
            maxScore = [score, word, potentialWordBag, potentialNextContainer]
    # If none of the words have options intersecting, it's time to backtrack
    if maxScore[0] == 0:
        return ["BACKTRACK", " ", " "]
    #Update the board by writing the chosen word into the board.
    #print(f"STEP Add to the board { maxScore[1]}") 
    #print(f"wordBag: {wordBag}")
    
    board = updateBoard(board, maxScore[1], container)
    retVal = [board, maxScore[2], maxScore[3]]

    #print(f"Return from best option: {retVal}")

    #Return board and the next wordbag and container and the current chosen word
    return [board, maxScore[2], maxScore[3]]
    

# Returns the total score for that word choice, wordbag for the intersecting element with minimum score, and the corresponding container 
def scoreAlgorithm(board, horizontal: bool, impactedBoxes: list, WORDLIST):
    #print("Score Algorithm")
    scoreSum = 0
    minScore = [sys.maxsize, " ", " "]

    # We are looking at the words which intersect the word shown by impactedBoxes. Thus, we need to flip the orientation
    horizontal = not horizontal
    for box in impactedBoxes:
        #print(box)

        #Check if this container is already filled
        potentialContainer = containerFromElement(board, box, horizontal)
        existUnfilled = False
        for coord in potentialContainer:
            if board[coord[0]][coord[1]] == " ":
                existUnfilled = True
        #This row/column has already been filled, so skip
        if not existUnfilled:
            continue


        [score, wordbag, container] = wordsThatFit(board, box, horizontal, WORDLIST)
        scoreSum += score

        if score < minScore[0]:
            minScore = [score, wordbag, container]
    
    return minScore
    
#Takes a single possible container and gets the score, wordbag and container
# Returns [score, wordbag, container]
def wordsThatFit(board, box, horizontal, WORDLIST):
    #print("wordsThatFit")
    container = containerFromElement(board, box, horizontal)
    #print(container)

    #Define a word frame and update it if there are existing characters
    wordFrame = ["."] * len(container)

    for i, coord in enumerate(container):
        if board[coord[0]][coord[1]] != " ":
            wordFrame[i] = board[coord[0]][coord[1]]
    
    #Find words which fit into this syntax via brute force single pass and regex
    stringTemplate = "".join(wordFrame)
    #print(f"The template {stringTemplate}")
    pattern = rf'{stringTemplate}'
    wordBag = []
    for key in WORDLIST.keys():
        if re.fullmatch(pattern, key):
            wordBag.append(key)
    
    score = len(wordBag)

    return [score, wordBag, container]
    
    



# Helper Functions
def checkBoardFull(board) -> bool:
    for row in board:
        for element in row:
            if element == ' ':
                return False
    return True

#Assuming board is full, check that this word results in a word in the opposite direction
def checkFullBoardCorrect(board, WORDLIST) -> bool:
     # Check Horizontal words
    for row in board:
        word = "".join(row)
        if word not in WORDLIST:
            return False
    
    # Get the vertical clues
    for j in range(len(board[0])):
        # Utilize a string builder using a list
        word = []
        for i in range(len(board)):
            word.append(board[i][j])
        word = "".join(word)

        if word not in WORDLIST:
            return False
        
    return True


# Container element are the coordinates of the element
def containerFromElement(board, containerElement, horizontal):
    #print("containerFromElement")
    dq = deque()
    dq.append([containerElement[0],containerElement[1]])

    row = containerElement[0]
    column = containerElement[1]

    if horizontal:
        #print("horizontal")
        #Move to the left
        while (column-1) >= 0:
            column -= 1
            dq.appendleft([row, column])
            #print("moving to the left")
            

        #Reset the column and move to the right
        column = containerElement[1]
        while (column+1) < len(board[0]):
            column += 1
            dq.append([row, column])
            #print("moving to the right")
        
    #Vertical 
    else:
        #print("vertical")
        #Move up
        while (row-1) >= 0:
            row -= 1
            dq.appendleft([row, column])
            #print("Row moving up")
            

        #Reset the column and move to the right
        row = containerElement[0]
        while (row+1) < len(board):
            row += 1
            dq.append([row, column])
            #print("Row moving down")
    retVal = list(dq)
    #Return the list of coordinates
    #print(f"retval of container {retVal}")
    return retVal


def chooseRandom(options: list):
    random_index = random.randint(0, len(options) - 1)
    return options[random_index]

def generateBoard(DIMENSION):
    board = []
    for i in range(DIMENSION):
        row = []
        for j in range(DIMENSION):
            row.append(" ")
        board.append(row)
    return board

def updateBoard(board, word, container):
    for i, coord in enumerate(container):
        board[coord[0]][coord[1]] = word[i]
    return board

def viewBoard(board):
    for row in board:
        print(row)


def run():
    #First fetch the data
    WORDLIST = getWords(FILEPATH)
    #print(WORDLIST)
    #print(type(WORDLIST))
    # Now generate a board
    emptyBoard = generateBoard(DIMENSION)

    # Now seed the board
    [board, firstWord] = initialSeed(emptyBoard, WORDLIST)

    # Begin the Loop. This will occur n+n-1 times (since we have already seeded the first)
    totalWordsToFind = 2 * DIMENSION -1 

    #Start with horizontal, specifically this first seeded line. 
    # wordBag at start is just the already chosen value
    # container is the specific cells impacted by the chosen word
    horizontal = True
    wordBag = [firstWord]
    # NOTE: Assumes container will always be in order!!
    container = [[0, i] for i in range(0, DIMENSION)]


    #Stack to store container, wordbag and board state for each step for backtracking (and horizontal cuz why not)
    copied_board = copy.deepcopy(board)
    stack = [[copied_board, wordBag, container, horizontal]]
    i = 0
    while i in range(totalWordsToFind):
        #print(f"Turn : {i}")
        # You get the wordBag and container
        [board, wordBag, container] = findBestOption(board, horizontal, wordBag, container, WORDLIST)
        #Update the horizontal
        horizontal = not horizontal

        #print(f"board value should be backtrack: {board}")
        #Backtrack by popping one off the stack
        if board == "BACKTRACK":
            #print("backtrack")
            i -= 1
            #You know that the n-1 directly meant n had to backtrack. Means you need to backtrack to the n-2
            discard = stack.pop()
            #print("discard")
            #print(discard)
            
            #NOTE You are not popping, since this becomes the next set of parameters, so you need to keep it in the stack
            test = stack[-1]

            #Check the counter: if greater than 5, means we have been here 5 times, so we need to backtrack again
            while test[4] >= 5:
                discard2 = stack.pop()
                #print("discard 2")
                #print(discard2)
                # update test
                test = stack[-1]
                i -= 1
            
            #Need to do a deep copy of the board otherwise will modify the values within the stack
            board = copy.deepcopy(test[0])
            wordBag = copy.deepcopy(test[1])
            container = copy.deepcopy(test[2])
            horizontal = copy.deepcopy(test[3]) # Probs don't need it for boolean, but curious to see what happens.


            # Update the counter for this element in the stack
            stack[-1][4] += 1
            #print(f"The counter is {stack[-1][4]}")


            #print([board, wordBag, container, horizontal, stack[-1][3]])
            #print("\n")
            #viewBoard(board)
            #print(f"The next chosen container is {container}")
            #print(f"The next chosen wordbags are {wordBag}")
            continue
        elif wordBag == "FINISHED":
            print("FINISHED BOARD")
            #print(board)
            break
        else:
            #Store this version onto the stack
            copied_board = copy.deepcopy(board)
            # Add a counter which will be appended each time the next word from this point fails
            #print(f"appending {[copied_board, wordBag, container, horizontal, 1]}")
            stack.append([copied_board, wordBag, container, horizontal, 1])


        #print("\n")
        #viewBoard(board)
        #print(f"The next chosen container is {container}")
        #print(f"The next chosen wordbags are {wordBag}")
        i += 1
    
        #need to consider special case of the last element
    return board
if __name__ == "__main__":
    run()