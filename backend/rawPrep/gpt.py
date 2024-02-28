# Assigns a difficulty and validates each of the clues

from dotenv import load_dotenv
import os
from openai import OpenAI
import json

# Load environment variables from .env file
load_dotenv()

# Access your API key
APIKEY = os.getenv('API_KEY')
FILEPATH = "./masterNYTList.txt"

# Initialize the OpenAI client with your API key
CLIENT = OpenAI(
  api_key= APIKEY
)

INSTRUCTION = "This GPT's role is to analyze a list of crossword words along with their clues, assigning difficulty levels from 1 (Monday NYT crossword level) to 7 (Sunday NYT crossword level)."
# REMOVED FROM INSTRUCTION: It evaluates the quality of the clues, identifying and returning any that are deemed bad or unsuitable for a New York Times style crossword puzzle. Clues are considered \"bad\" if they are not easily answerable by the GPT given its knowledge and context, indicating a lack of clarity or specificity necessary for a quality clue. The GPT communicates in a straightforward, concise manner, without needing to explain the reasoning behind the difficulty level or identification of a clue as bad, focusing on maintaining the integrity and style of NYT crossword puzzles
RETURNFORMAT = "Return the difficulty level of this clue given. Return only a single number from 1 to 7"
# REMOVED FROM INSTRUCTION: Return the answer in json mode, with the key being the word, and the value being a list with each element being a tuple consisting of a clue and its difficulty level. Note that there can be multiple clues for each word. Example: \"word\" : [[\"sample clue 1\", 1], [\"sample clue 2\", 5], [\"sample clue 3\", 7]]. Make sure to format it properly
PROMPT = "Given the following input, assign this clue a difficulty level. Again, return only a single nubmer from 1 to 7. Do not include any text in your answer. Only return a single number which should be a single token. "

#REMOVED FROM PROMPT: Remove clues from the returning json which you deem to be \"bad\" clues as specified by the instructions, but don't be too aggressive. Make sure not to include any newline characters

# sampleData = """
# "AALTO": [
#         "Finlandia House architect",
#         "Architect Alvar ___",
#         "Designer Alvar",
#         "Alvar who designed Finlandia Hall",
#         "Finnish architect Alvar ___",
#         "Noted Finnish chair designer"
#     ],
#     "AANDE": [
#         "\"Duck Dynasty\" network",
#         "Cable network specializing in \"real life\" shows",
#         "Owner of the History Channel",
#         "Former \"Biography\" channel",
#         "\"Biography\" network, once",
#         "Sister of the Biography Channel",
#         "Owner of The History Channel",
#         "\"Panic 911\" airer",
#         "Cable choice",
#         "Cable channel",
#         "\"Billy the Exterminator\" network",
#         "\"Biography\" channel",
#         "\"Biography\" network",
#         "\"Hoarders\" airer"
#     ],
#     "AANDP": [
#         "U.S.'s first grocery chain",
#         "Food chain?",
#         "1961 John Updike story set in a grocery store",
#         "Kroger competitor",
#         "Supermarket chain"
#     ],
#     "AARGH": [
#         "Cry of exasperation",
#         "\"Good grief!\"",
#         "\"Why is this happening to me?!\"",
#         "[Why me?!]",
#         "Exasperation exclamation",
#         "Cry of frustration"
#     ],
#     "AARON": [
#         "Brother of Moses",
#         "Biblical miracle-maker",
#         "Baseball record-setter of 4/8/74",
#         "Hank who hit 755 homers",
#         "R.B.I. recordholder",
#         "___ Burr, major role in \"Hamilton\"",
#         "One of a pair of biblical brothers",
#         "All-time leader in R.B.I.'s",
#         "With whom Moses went to Egypt",
#         "Baseball All-Star every year from 1955 to 1975",
#         "Super Bowl XLV M.V.P. Rodgers",
#         "Golden calf builder",
#         "Moses' older brother",
#         "___ Paul, Emmy winner for \"Breaking Bad\"",
#         "Golden calf's maker",
#         "Hitter of 755 home runs",
#         "Hank whose home-run record was surpassed by Barry Bonds",
#         "All-time leader in r.b.i.'s",
#         "\"The Boondocks\" cartoonist McGruder",
#         "Home run king Hank",
#         "Golden calf crafter",
#         "Man with a rod, in the Bible",
#         "Screenwriter Sorkin",
#         "First high priest of the Israelites",
#         "1973 Masters winner Tommy",
#         "Slugger with 755 home runs",
#         "First first name?",
#         "\"The Ten Commandments\" role",
#         "Boy's name that's almost always first alphabetically",
#         "Duelist Burr",
#         "He slew Alexander",
#         "Sorkin who created HBO's \"The Newsroom\"",
#         "Pop singer Neville",
#         "Oscar winner Sorkin",
#         "Vice President Burr",
#         "Hammerin' Hank",
#         "Singer ___ Neville",
#         "Successor of Ruth",
#         "Claire's boy on \"Lost\"",
#         "Name likely to come first in a class roll call",
#         "First player listed in \"Total Baseball\"",
#         "Husband of Elisheba",
#         "First name alphabetically in the Baseball Hall of Fame",
#         "Sorkin who wrote \"The Social Network\"",
#         "First Baseball Hall-of-Famer, alphabetically",
#         "Alphabetically first name in the Bible",
#         "Sorkin who created \"The West Wing\"",
#         "Hank with the retired #44",
#         "*Brother of Moses",
#         "Baseball's \"Hammerin' Hank\"",
#         "Singer Neville",
#         "Moses' brother",
#         "TV producer Spelling",
#         "Father of Eleazar, in the Bible",
#         "Baseball's Hammerin' Hank",
#         "Early priest",
#         "Composer Copland",
#         "Spelling of TV",
#         "Hitter known as The Hammer",
#         "Newsman Brown",
#         "Biblical wonder worker",
#         "Hebrews' first high priest",
#         "Perennial N.L. leader of old"
#     ],
#     "ABABA": [
#         "Quintain rhyme scheme",
#         "Part of a capital's name meaning \"flower\"",
#         "Addis ___",
#         "Addis ___, Ethiopia",
#         "Half a world capital"
#     ],
#     "ABARN": [
#         "Can't hit the broad side of ___"
#     ],
#     "ABASE": [
#         "Bring down",
#         "Belittle",
#         "Lower in rank",
#         "Put to shame",
#         "Take down a notch",
#         "Take down a peg",
#         "Put down",
#         "In lower rank",
#         "Lower",
#         "Knock down a peg",
#         "Degrade",
#         "Demean",
#         "Humiliate",
#         "Treat like dirt",
#         "Humble"
#     ],
#     "ABASH": [
#         "Discountenance",
#         "Put to shame",
#         "Make ashamed",
#         "Embarrass",
#         "Discomfit",
#         "Discompose",
#         "Ruffle",
#         "Cause to blush",
#         "Bring shame to",
#         "Disconcert",
#         "Leave red-faced",
#         "Shame",
#         "Make red-faced"
#     ],
#     "ABATE": [
#         "Wane",
#         "Ebb away",
#         "Ease up",
#         "Die down",
#         "Lose intensity",
#         "Stem",
#         "Subside",
#         "Drop off",
#         "Tail off",
#         "Lower",
#         "Ease",
#         "Fall off",
#         "Slacken",
#         "Weaken",
#         "Go down",
#         "Diminish",
#         "Let up",
#         "Diminish in strength",
#         "Moderate",
#         "Taper off",
#         "Lessen",
#         "Peter out"
#     ],

 

# """

#Too hard to query with buffers; api call one clue at a time.



def apiCall(buffer):
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        #response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"{INSTRUCTION}"},
            {"role": "system", "content": f"{RETURNFORMAT}"},
            {"role": "user", "content": f"{PROMPT}"},
            {"role": "user", "content": f"Here is the data: {buffer}"}
        
        ]
    )

    content = response.choices[0].message.content

    # Deserialize the JSON content to a Python dict
    print(content)
    
    content_dict = json.loads(content)
    try:
        test = int(content_dict)
        return content_dict
    except:
        #Assign temp number
        return 3
    
  
    

def appendFile(file_path, key, value):
    with open(file_path, 'a') as file:  # Open the file in append mode
        # Prepare the string to append
        entry_str = json.dumps({key: value}) + '\n'  # Convert the dictionary to a JSON string and add a newline
        file.write(entry_str)  # Append the string to the file

def main():
    #This is just a sort of test
    #print(type(apiCall(sampleData)))


    # First open the file 
    with open(FILEPATH, 'r') as file:
        data = json.load(file)
    

    finalDict = {}
    tempDict = {}

    filename = "difficultyMasterNYTList.txt"

    # Flush the buffer to openAI once it hits a certain limit 
    # Based on testing, buffer size of 4k is most optimal
    # buffer = ""

    #Buffer doesn't work because output is too variable from gpt 3.5 Need to do it line by line
    apiCounter = 0
    with open('output.txt', 'a') as file:
        reached = False
        for key in data:
            if key == "APEEP":
                reached = True
            
            if not reached:
                continue
            print(f"The number of API calls is {apiCounter}")
            tempDict = {}
            tempDict[key] = []
            # buffer += f"\"{key}\": [\n"
            # for clue in data[key]:
            #     buffer += f"\t \"{clue}\",\n"
                
            # buffer += "],\n"
            # if len(buffer) > 500:
            #     #call the api 
            #     tempDict = dict(apiCall(buffer))
            #     print(json.dumps(tempDict, indent=4))
            #     finalDict.update(tempDict)
            #     buffer = ""
            #     apiCounter += 1
            for clue in data[key]:
                

                inputText = f"{key} : {clue}"
                difficulty = int(apiCall(inputText))
                apiCounter += 1
                tempDict[key].append([clue, difficulty])
            
            #Update the finalDict with this tempDict
            finalDict.update(tempDict)

            #Put contents of tempDict into file
            appendFile(filename, key, tempDict[key])


    # Technically I don't even need the final dict.

    #Write the finalDict to a text file
    
    # with open(filename, 'w') as f:
    #     for key, value in finalDict.items():
    #         f.write(f'{key}: {value}\n')
    

if __name__ == "__main__":
    main()
