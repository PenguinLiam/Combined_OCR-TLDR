
#   VARIABLES    #

# =========================================================================== #
'''
File used to hold any variable data and basic functions that didn't make 
sense/were more complex to put into pther files. Comments are attempted to be 
written in accordance with PEP 8 Style Guide: 
http://legacy.python.org/dev/peps/pep-0008/#comments
https://google.github.io/styleguide/pyguide.html
'''
# =========================================================================== #


# ====== Imports (Python Native Modules and My Program Modules) ====== #

import pickle
import time



# ====== Variable definitions ====== #

# All of the letters and numbers to compare each character to - Numbers included
# for statistics, etc. in texts.
alphabet = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g',
           'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n',
           'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u',
           'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', '0', '1', '2', '3',
           '4', '5', '6', '7', '8', '9', ' ']

# A basic set of words which the system will not give a score to when ranking
# words. Also used as a naive spell check for OCR conversions.
# Must be lower case. Words may be added.
notAcceptedWords = ["the", "of", "to", "and", "a", "in", "is", "it", "you",
                    "that", "he", "was", "for", "on", "are", "with", "as", "i",
                    "his", "they", "be", "at", "have", "this", "from", "or",
                    "had", "by", "while", "where", "after", "so", "though",
                    "since", "until", "do", "there"]

# Current date
date = str(time.strftime("%d-%m-%Y"))

# Default settings - changes when settings.txt is loaded
settings = {"noOfDays":30, "noOfSummaries":1, "noOfOCRs":1}



# ====== Save & Load Sub-Routines ====== #

def save():
    '''Saves settings to settings.txt.'''
    with open("settings.txt", "wb") as f:
        pickle.dump(settings, f)

def load():
    '''Loads settings from settings.txt.'''
    global settings
    with open("settings.txt", "rb") as f:
       settings = pickle.load(f)



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    print("This file cannot be run as main...")
    input()