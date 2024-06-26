import pandas as pd


# This data is used to test the Naive Bayes algorithm
# The first number in the list is the number of times the word appears in ham (not smap) emails, while the second number is the number of times the word appears in spam emails
hamSpamData = {
    "fortune" : [0, 375],
    "next" : [125, 0],
    "programming" : [250, 0],
    "money" : [0, 750],
    "you" : [125, 375]
}

verboseSingleProb = True

hamProb = 250
spamProb = 750

def calculateIndividualProbabilities(wordsData, emailType):
    cardinality = 2

    wordsFalseProbabilities = []
    wordsTrueProbabilities = []
    for word in wordsData:
        countHam = wordsData[word][0]
        countSpam = wordsData[word][1]
        print(f"\nWORD: {word}, Count Spam: {countSpam}, Count Ham: {countHam}")

        if emailType == "ham": # False spam
            wordProbabilityTrue = (1 + countHam) / (cardinality + hamProb)
            wordProbabilityFalse = 1 - ((1 + countHam) / (cardinality + hamProb))
        else: # True spam
            wordProbabilityTrue = (1 + countSpam) / (cardinality + spamProb)
            wordProbabilityFalse = 1 - ((1 + countSpam) / (cardinality + spamProb))

        if verboseSingleProb : print(f"Probability of word '{word}' false in {emailType}emails: {str(wordProbabilityFalse)} and true: {str(wordProbabilityTrue)}")

        wordsFalseProbabilities.append(round(wordProbabilityFalse, 3))
        wordsTrueProbabilities.append(round(wordProbabilityTrue, 3))
    
    return wordsFalseProbabilities, wordsTrueProbabilities

# Test the Naive Bayes algorithm
falseProbsHam, trueProbsHam = calculateIndividualProbabilities(hamSpamData, "ham")
falseProbsSpam, trueProbsSpam = calculateIndividualProbabilities(hamSpamData, "spam")

probsData = {
    "falseProbsHam" : falseProbsHam,
    "trueProbsHam" : trueProbsHam,
    "falseProbsSpam" : falseProbsSpam,
    "trueProbsSpam" : trueProbsSpam
}

df = pd.DataFrame(probsData)
print(df)