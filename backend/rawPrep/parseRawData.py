import csv
import json

# Macro list of lengths you want the word to be
LENGTHS = [5]


tsv_file_path = './clues.tsv'

word2Clue = {}

counter = 0
# Open the TSV file for reading
with open(tsv_file_path, 'r') as file:
    # Create a CSV reader specifying the delimiter as a tab character
    tsv_reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
    
    # Iterate over each row in the TSV file
    for row in tsv_reader:
        # From NYT, later than 2000, and 5 letters long
        if row[0] == "nyt" and int(row[1]) > 1999 and len(row[2]) in LENGTHS:
            counter += 1

            # Remove words with puzzle-specific clues
            if "-Down" in row[3] or "-Across" in row[3]:
                continue

            #Multiple clues per word
            if row[2] in word2Clue:
                word2Clue[row[2]].add(row[3])
            else:
                # List of clues to go with each word
                word2Clue[row[2]] = set([row[3]])

#Add this key to know the content size of this hashmap


word2Clue["THE_SIZE"] = set([counter])
print(word2Clue)
print(counter)

# Turn the sets back into lists so that it is JSON serializable
for key in word2Clue:
    word2Clue[key] = list(word2Clue[key])

# Specify the file path
file_path = './masterNYTList.txt'

# Open the file for writing
with open(file_path, 'w') as file:
    # Write the dictionary to the file as JSON
    json.dump(word2Clue, file, indent=4)

