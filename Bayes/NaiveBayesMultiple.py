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
totalEmails = hamProb + spamProb

verboseIndividualProbs = False

def calculateNaiveBayes(wordsData, emailType):
    cardinality = len(wordsData)

    print("\n\nGetting the probability of the email being " + emailType)
    # Probability is set to 1 as Naive Bayes assumes independence between the words
    probability = 1.0

    wordsProbabilities = []
    for word in wordsData:
        countHam = wordsData[word][0]
        countSpam = wordsData[word][1]
        print(f"\nWORD: {word}, Count Spam: {countSpam}, Count Ham: {countHam}")

        if emailType == "ham": # False spam
            wordProbability = (1 + countHam) / (cardinality + hamProb)
        elif emailType == "spam": # True spam
            wordProbability = (1 + countSpam) / (cardinality + spamProb)
        if verboseSingleProb : print(f"Probability of word '{word}' in {emailType} emails: {str(wordProbability)}")

        wordsProbabilities.append(round(wordProbability, 3))

        probability *= wordProbability

    # Apply the prior only once per classification, outside the loop
    if emailType == "ham":
        prior = hamProb / totalEmails
    elif emailType == "spam":
        prior = spamProb / totalEmails
    
    probability *= prior

    return probability, wordsProbabilities

# Test the Naive Bayes algorithm
probHam, wordsProbsHam = calculateNaiveBayes(hamSpamData, "ham")
probSpam, wordsProbsSpam = calculateNaiveBayes(hamSpamData, "spam")

print(f"\n\nProbability of the email being ham: {probHam}")
print(f"Probability of the email being spam: {probSpam}")

# Create a dictionary with the results
data = {
    "probsHam" : wordsProbsHam,
    "probsSpam" : wordsProbsSpam,
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
if verboseIndividualProbs : print(df)