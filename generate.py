"""
Samuel Hohenshell
06/18/20

Produces a string of a given length based on what is learned from the given
dictionary AKA markov chain file.

NOTE: This can be implemented in many different ways, I just chose this way 
but it can be very easily altered.

Command call format: 
> python3 generate.py <number_of_words_to_generate> <dictionary>
"""

import sys, os, random, json

def main():
    n, filename = read_arguments()
    markov_chain = load_dict(filename)

    last_word = "~~~~~~~~~~~~"  # Holds the previous word that was generated
    result    = ""              # Stores the string we are building
    new_word  = ""              # Will store current AKA the new word generated
    
    # Generating "n" number of words
    for i in range(0, n):
        # Generating the next word
        new_word = get_next_word(last_word, markov_chain)
        # Updating the result string
        result = result + " " + new_word
        # Storing current word as last word to prepare for next generation
        last_word = new_word

    print(result)


# Generates the next word for the string
def get_next_word(last_word, mc):
    if last_word not in mc:
        # Pick a random new "state" AKA starting word
        rand_num = random.randint(0, len(mc) - 1)
        return (list(mc.keys())[rand_num])
    else:
        # Pick a word from the list of words that come after last_word
        candidates = mc[last_word]
        candidates_normalized = []  # Scaled version of candidates
        # Filling candidates_normalized based on frequency of each word
        for word in candidates:
            frequency = candidates[word]
            for i in range(0, frequency):
                candidates_normalized.append(word)
        # Gathering a random string from the normalized list and returning it
        rand_num = random.randint(0, len(candidates_normalized) - 1)
        return candidates_normalized[rand_num]


# Reads in the arguments and returns them (or default values)
def read_arguments():
    # Setting default values
    length = 50
    filename = "dict.json"

    # Checking arguments to see if non-defaults were provided
    if (len(sys.argv) >= 2):
        if ((sys.argv[1]) == "-h") or ((sys.argv[1]) == "--help"):
            print("Command call format: \n> python3 generate.py "\
                "<number_of_words_to_generate> <dictionary>")
            exit()
        length = int(sys.argv[1])
    if (len(sys.argv) >= 3):
        filename = sys.argv[2]

    return length, filename


# Loads the dictionary from the given json filepath
def load_dict(filename):
    # If dictionary file doesn't exist, exit
    if not os.path.exists(filename):
        sys.exit("ERROR: Dictionary/Markov Chain file \"" + filename +
            "\" not found. Exiting...")
    with open(filename, "r") as json_file:
        # Load in the markov chain from the dictionary and return it
        file_as_string = json_file.read()
        data = json.loads(file_as_string)
    return data


if __name__ == "__main__":
    main()