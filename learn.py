"""
Samuel Hohenshell
06/18/20

Command line call format: 
> python3 learn.py <dictionary_name> <input_file_name>
    - dictionary_name: json file to store the markov chain in 
        - defaults to dict.json
    - input_name: document to learn from
        - defaults to interactive mode
"""

import sys, json
import os.path

def main():
    # Reading the user args
    dict_file, inp_file = read_args()
    # Loading in the json dictionary AKA our Markov Chain
    markov_chain = load_dict(dict_file)

    # If input file wasn't given, learn from user input (interactive mode)
    if inp_file == "":
        print("\nEnter as much text as you would like your chatbot to learn "\
            "from. When you are done, just enter a blank line.\n")
        while True:
            user_input = input("_-¯-_-¯-_-¯-> ")
            if user_input == "":
                break
            markov_chain = learn(markov_chain, user_input)
            update_file(dict_file, markov_chain)
    
    # Else, input file is given, learn from given file
    else:
        with open(inp_file, "r") as file: 
            file_as_string = file.read()
            markov_chain = learn(markov_chain, file_as_string)
            update_file(dict_file, markov_chain)



# Returns filename for dictionary file, filename for input file
def read_args():
    # Default values
    dictionary_file = "dict.json"
    input_file = ""

    # Reading in values
    if (len(sys.argv)) >= 2:
        if ((sys.argv[1]) == "-h" ) or ((sys.argv[1]) == "--help"):
            print("Command call format: \n> python3 learn.py "\
                "<dictionary_name> <input_file_name>")
            exit()
        dictionary_file = sys.argv[1]
    if (len(sys.argv)) >= 3:
        input_file = sys.argv[2]

    return dictionary_file, input_file


# Loads the dictionary from the given json filepath
def load_dict(filename):
    # If dictionary file doesn't exist, create it as an empty json file
    if not os.path.exists(filename):
        with open(filename, "w") as json_file:
            json.dump({}, json_file)
    with open(filename, "r") as json_file:
        # Load in the markov chain from the dictionary and return it
        file_as_string = json_file.read()
        data = json.loads(file_as_string)
    return data


# Updates the given dictionary based on the string input
def learn(dictionary, inp):
    # dictionary: The current dictionary representing our markov chain
    # input: The input used to analyze/learn from
    inp = inp.replace("\n", " ")  # Replacing all newlines with spaces
    # NOTE: The above operation makes this run in O(n^2), I'm sure there is 
    #   a better fix but I don't care enough to implement it right now
    tokens = inp.split(" ")       # Splitting input by spaces or newlines
    for i in range (0, len(tokens) - 1):
        curr_word = tokens[i]
        next_word = tokens[i+1]
        # If current word is not in the dictionary, add and initialize it
        if curr_word not in dictionary:
            dictionary[curr_word] = { next_word : 1}
        # If current word in dictionary, update it
        else:
            all_next_words = dictionary[curr_word]
            # If the next word is not in the list of next words, add it
            if next_word not in all_next_words:
                dictionary[curr_word][next_word] = 1
            # If the next word is in the list of next words, increment it
            else:
                dictionary[curr_word][next_word] += 1
    return dictionary


# Write the given dictionary to the json at "filename" 
def update_file(filename, dictionary):
    with open(filename, "w") as json_file:
        json.dump(dictionary, json_file)


if __name__ == "__main__":
    main()
