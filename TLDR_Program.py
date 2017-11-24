
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

import Variables as v
import sys
import os
import time


# ====== Main TLDR Class ====== #

class Summary:
    '''Class for carrying out Too Long; Didn't Read functions.

    Class within which all of the summary tools reside. Receives text input
    (main text, and title). Splits the text into sentences, then words and then
    ranks each word based on occurence and whether it appears in the title.
    Totals the score of sentences based on score of words and then places best
    sentences in order of their placement in the original text.
    '''

    def save(self, summaryOut):
        '''Saves the summarised texts to the Summaries folder.

        Encodes saved files in UTF-8 Format - non-UTF-8 characters cannot be
        saved.
        
        Attributes:
            summaryNumber: The number of previous summaries + 1
            completeName: File name in the format of Summary_#_date.txt
            toFile: What to write to the file

        Raises:
            Exception: Any errors flagged and printed
        '''
        try:
            print("SAVING...")
            summaryNumber = str(v.settings["noOfSummaries"])
            completeName = ("Summary_#"+summaryNumber+"_"+v.date+".txt")
            with open(os.path.join('Summaries', completeName), "w", encoding="utf-8") as file:
                toFile = summaryOut
                file.write(toFile)
            v.settings["noOfSummaries"] += 1
            v.save()
            print("SAVED...")
        except Exception as e:
            print(e)
        return

    def split_sentence(self, text):
        '''Splits the text into sentences.

        Removes extra whitespace, splits into sentences and then removes
        non-alpha-numeric characters. Uses original text as source.

        Attributes:
            text: The original text
            sentences: A list containing split sentences

        Returns:
            List containing the formatted sentences, number of sentences and 
            original sentences without edits
        '''
        # Removes extra whitespace
        text = text.splitlines()
        text = '. '.join(text)
        text = text.split(". ")
        sentencesSplit = []
        for i in text:
            i = i.split(". ")
            sentencesSplit.extend(i)
        noOfSentences = len(sentencesSplit)
        # Cycling through each character of each word and remove them if they're
        # not in 'v.alphabet'
        sentences = []
        for i in sentencesSplit:
            for j in i:
                if j not in v.alphabet:
                    i = i.replace(j, '')
            sentences.append(i)
        sentenceData = [sentences, noOfSentences, sentencesSplit]
        return sentenceData

    def rank_words(self, sentences, title):
        '''Ranks words based on occurence in text and whether they appear in the
        title.
        
        Adds 1 point for each time a word appears in the text and 3 for if it
        appears in the title. Doesn't add a score for conjunctives 
        (v.notAcceptedWords) to make sentence scoring more accurate. Uses the
        split sentences and the title as sources.

        Attributes:
            tTokens: The words in the title
            Tokens: The words in the text
            wordScore: Dictionary of words and their corresponding scores

        Returns:
            List containing a dictionary of words from the text and their
            corresponding scores... For example:
            {'lower': 36, 'case': 14, 'words': 23}
            ... and the number of words in the text:
        '''
        # Removing any non alpha-numerical characters from the title
        for i in title:
            if i not in v.alphabet:
                title = title.replace(i, '')
        # Making words lower case to prevent mis-matches for the same word, but
        # with different case structures
        tTokens = title.split(" ")
        tokens = []
        for i in sentences:
            i = i.split(" ")
            tokens.extend(i)
        noOfWords = len(tokens)
        # Searching through every word/token in the text to identify the words
        # and add them to the dictionary with a score 
        wordScore = {}
        for i in tokens:
            if i in wordScore.keys():
                wordScore[i] += 1
            elif i in v.notAcceptedWords: 
                continue
            else:
                wordScore[i] = 1        # Adds 1 if the word occurs in text
        # Compares words in the title to words in the dictionary
        for i in tTokens:
            if i in wordScore.keys():
                wordScore[i] += 3       # Adds 3 if the word is in the title
            else:
                continue
        wordData = [wordScore, noOfWords]
        return wordData

    def rank_sentences(self, sentences, wordRank):
        '''Ranks sentences based on the sum of the score of the words in the
        sentence.

        Adds the score of each word in the sentence that is also in wordScore.
        Any sentences that are less than 6 words long are discounted. Uses the
        split sentences and wordRank as sources.
        
        Attributes:
            sentenceScore: Dictionary containing sentences and their
                corresponding scores
            tokens: The words in each sentence

        Returns:
            Dictionary containing eac sentence and their corresponding scores.
            For example:
            {'this is a sentence of more than 6 words': 23,
            'this is another sentence of more than 6 words': 27}
        '''
        sentenceScore = {}
        # Searches through each word in each sentence, comparing it to the 
        # wordRank dictionary and applying the number of points ascociated with
        # that word to the sentencesScore (value)
        for i in sentences:
            tokens = i.split(' ')
           # Removes 'unimportant sentences' - ones with less than 6 words
            if len(tokens) < 6:
                continue
            # Searching through each word and comparing to 'wordRank'
            for j in tokens:
                if j in wordRank.keys():                        
                    if i not in sentenceScore:
                        sentenceScore[i] = wordRank[j]
                    else:
                        sentenceScore[i] += wordRank[j]
        return sentenceScore

    # Works out which sentences to print and the order in which to print them 
    def form_summary(self, text, sentenceRank, summaryAmount, sentences, rawSentences):
        '''Forms a summary from the ranked sentences of the length specified
        by summaryLength.

        Sorts the ranked sentences from highest to lowest scoring (values) with
        the native python worting function. The identifies the sentences in the
        original text and retrieves their indexes and prints the corresponding
        sentences from the original text (to get original formatting and
        all characters in original sentence.

        Attributes:
            summary: The final summary of the text
            finalSentences: Dictionary containing the highest ranked sentences
                and index in original text
            sortedFinalSentences: X number of highest ranked sentences in the
                original text order

        Returns:
            String containing the final summary of the text
        '''
        # Sorts the sentences by score (dictionary value)
        from operator import itemgetter 
        sorted_x = sorted(sentenceRank.items(), key=itemgetter(1), reverse=True)
        # Retrieves the summaryAmount highest ranked sentences
        lst = [i[0] for i in sorted_x]
        finalSentences = {}
        summary = lst[:(summaryAmount)]
        for i in summary:
            finalSentences[i] = sentences.index(i)
        # Sorts the final sentences by index in original text
        sortedFinalSentences = sorted(finalSentences.items(), key=itemgetter(1), reverse=False)
        rawSentenceNumbers = [i[1] for i in sortedFinalSentences]
        print(rawSentenceNumbers)
        summary = [rawSentences[i] for i in rawSentenceNumbers]
        summary = [i.capitalize() for i in summary]
        summary = ". ".join(summary)        
        return summary

    def summarise(self, title, text, summaryAmount):
        '''Main function for controling summary class.
        
        Calls each sub-routine within the class to carry out the necessary
        functions for summarising the given text.

        Attributes:
            rawSentences: Sentences in text with all grammar remaining
            wordRank: Dictionary of scoring words with their corresponding score
            SentenceRank: Dictionary of sentences with their corresponding score
            summaryOut: Final summary to be returned
            [... Others are self explanatory]

        Returns:
            String containing the final summary of the text
        '''
        # Splitting to sentences
        sentenceBack = self.split_sentence(text)
        sentences = sentenceBack[0]
        noOfSentences = sentenceBack[1]
        rawSentences = sentenceBack[2]

        # Ranking words based on occurance and whether they are in the title
        wordBack = self.rank_words(sentences, title)
        wordRank = wordBack[0]
        noOfWords = wordBack[1]

        # Ranking sentences based on the sum of the score of their words
        sentenceRank = self.rank_sentences(sentences, wordRank)
        
        # Finding how many sentences to print and then identifying those
        # sentences to form the final summary
        summaryOut = self.form_summary(text, sentenceRank, summaryAmount, sentences, rawSentences)

        # Saves the summarised text into a .txt format
        self.save(summaryOut)
        return summaryOut



# ====== Main Sub-Routine ====== #

def main(title, text, summaryAmount):
    '''Main referral sub-routine for TLDR program'''
    summaryAmount = int(summaryAmount)
    title = title.lower()
    text = text.lower()
    # Defines the class Summary as an object
    S = Summary()
    summaryOfText = S.summarise(title, text, summaryAmount)
    return summaryOfText



# ====== Python Boiler Plate ====== #

if __name__ == "__main__":
    '''Asks for inputs if not called by another module'''
    title = input("Enter the title: ")
    text = input("Enter some text to be summarised: ")
    summaryAmount = input("How many sentences should the text be summarised into?: ")
    main(title, text, summaryAmount)
