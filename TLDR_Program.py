
#   TL;DR PROGRAM    #

# =========================================================================== #
'''
Program for summarising the text supplied by user or from the OCR completed 
text folder. Comments are attempted to be written in accordance with PEP 8 
Style Guide: 
http://legacy.python.org/dev/peps/pep-0008/#comments
https://google.github.io/styleguide/pyguide.html
'''
# =========================================================================== #



# ====== Imports (Python Native Modules and My Program Modules) ====== #

from operator import itemgetter
import Encryption as E
import Variables as v
import time
import sys
import os



# ====== Main TLDR Class ====== #

class Summary:
    '''Class for carrying out Too Long; Didn't Read functions.

    Class within which all of the summary tools reside. Receives text input
    (main text, and title) and the amount of sentences into which the text is
    summarised. Splits the text into sentences, then words and then
    ranks each word based on occurence and whether it appears in the title.
    Totals the score of sentences based on score of words and then places best
    sentences in order of their placement in the original text.
    '''
    def __init__(self, title, text, summaryAmount):
        '''Inits the class. Assigns all the object wide variables.'''
        self.text = text.lower()
        self.title = title.lower()
        self.summaryAmount = summaryAmount
        self.split_to_sentences()

    def summarise(self):
        '''Calls each of the residing functions within the class for the summary
        process.
        
        Returns:
            String containing the final summary.'''
        self.rank_words()
        self.rank_sentences()
        self.form_summary()
        self.save()
        return self.summary
        
    def split_to_sentences(self):
        '''Splits text into sentences.

        Removes whitespace and non-alpha-numerical characters.

        Attributes:
            self.rawSentences: Sentences containing all their punctuation marks
            self.sentences: The pure alpha-numerical sentences
        '''
        self.text = " ".join(self.text.splitlines())
        self.rawSentences = self.text.split(". ") 

        self.sentences = []
        for sentence in self.rawSentences:
            for word in sentence:
                for character in word:
                    if character not in v.alphabet:
                        sentence = sentence.replace(character, "")
            self.sentences.append(sentence)

    def rank_words(self):
        '''Ranks words based on occurence in text and whether they appear in the
        title.

        Adds 1 point for each time a word appears in the text and 3 for if it
        appears in the title. Doesn't add a score for conjunctives 
        (v.notAcceptedWords) to make sentence scoring more accurate. Uses the
        split sentences and the title as sources.

        Attributes:
            words: Each word in the text
            titleWords: Each word in the title
            self.wordScore: Dictionary of words and their corresponding scores
        '''
        for character in self.title:
            if character not in v.alphabet:
                self.title = self.title.replace(character, "")

        titleWords = self.title.split(" ")

        words = []
        for sentence in self.sentences:
            words.extend(sentence.split(" "))

        self.wordScore = {}
        for word in words:
            if word in self.wordScore.keys():
                self.wordScore[word] += 1
            elif word in v.notAcceptedWords:
                continue
            else:
                self.wordScore[word] = 1

        for word in titleWords:
            if word in self.wordScore.keys():
                self.wordScore[word] += 3

    def rank_sentences(self):
        '''Ranks sentences based on the sum of the score of the words in the
        sentence.

        Adds the score of each word in the sentence that is also in wordScore.
        Any sentences that are less than 6 words long are discounted. Uses the
        split sentences and wordRank as sources.

        Attributes:
            self.sentenceScore: Dictionary of sentences and their corresponding
                scores
            words: List of words in each sentence
        '''
        self.sentenceScore = {}
        for sentence in self.sentences:
            words = sentence.split(" ")
            if len(words) < 6:
                continue
            for word in words:
                if word in self.wordScore.keys():
                    if sentence not in self.sentenceScore:
                        self.sentenceScore[sentence] = self.wordScore[word]
                    else:
                        self.sentenceScore[sentence] += self.wordScore[word]

    def form_summary(self):
        '''Forms a summary from the ranked sentences of the length specified
        by summaryLength.
        
        Sorts the ranked sentences from highest to lowest scoring (values) with
        the native python worting function. Identifies the sentences in the
        original text and retrieves their indexes and prints the corresponding
        sentences from the original text (to get original formatting and
        all characters in original sentence).
        
        Attributes:
            orderedSentences: Scored sentences ordered by their scores
            finalSentences: The X number of higest ranked sentences
            sentenceIndex: Top ranked sentences and their indexes in the 
                original text
            sortedFinalSentences: Top ranked sentences ordered by their index
            self.summary: Final summary output
        '''
        orderedSentences = sorted(self.sentenceScore.items(), key=itemgetter(1), reverse=True)
        orderedSentences = [i[0] for i in orderedSentences]
        finalSentences = orderedSentences[:int(self.summaryAmount)]
                 
        sentenceIndex = {}
        for sentence in finalSentences:
            sentenceIndex[sentence] = int(self.sentences.index(sentence))

        sortedFinalSentences = sorted(sentenceIndex.items(), key=itemgetter(1), reverse=False)
        sentenceIndexes = [i[1] for i in sortedFinalSentences]
        
        self.summary = [self.rawSentences[i] for i in sentenceIndexes]
        self.summary = [i.capitalize() for i in self.summary]
        self.summary = (". ".join(self.summary)+".")

    def save(self):
        '''Saves the summarised texts to the Summaries folder.

        Encodes saved files in UTF-8 Format - non-UTF-8 characters cannot be
        saved.
        
        Attributes:
            summaryNumber: The number of previous summaries + 1
            completeName: File name in the format of Summary_#_date.txt

        Raises:
            Exception: Any errors flagged and printed
        '''
        try:
            summaryNumber = str(v.settings["noOfSummaries"])
            completeName = ("Summary_#" + summaryNumber + "_" + v.date + ".txt")
            with open(os.path.join('Summaries', completeName), "w", encoding="utf-8") as file:
                file.write(E.encrypt(self.summary))
            v.settings["noOfSummaries"] += 1
            v.save()
        except Exception as e:
            print(e)



# ====== Main Sub-Routine ====== #

def summarise(title, text, summaryAmount):
    S = Summary(title, text, summaryAmount)
    return S.summarise()



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    try:
        title = input("ENTER A TITLE FOR THE TEXT: ")
        text = input("ENTER SOME TEXT TO BE SUMMARISED: ")
        summaryAmount = input("ENTER A AMOUNT OF SENTENCES FOR SUMMARY: ")
        print(summarise(title, text, summaryAmount))
        input()
    except Exception as e:
        print(e)
        input()
