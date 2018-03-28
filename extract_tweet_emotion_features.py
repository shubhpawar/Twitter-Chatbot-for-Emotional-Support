import nltk
import numpy as np
import pandas as pd
import re
from textblob import TextBlob

#Creating a dictionary of ANEW words
anew = []
anew = pd.read_excel("Data/ANEW.xlsx")
anewDict = dict()
i = 1
for i in range(1,anew['Word'].size+1):
    anewDict[anew['Word'][i]] = anew['V.Mean.Sum'][i]

emoji_pattern = re.compile(
    "(\ud83d[\ude00-\ude4f])|"  # emoticons
    "(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    "(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    "(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    "(\ud83c[\udde0-\uddff])|"  # flags (iOS)
    "(\U0001f602)"
    "+", flags=re.UNICODE)

#Calculating valence scores for each tweet and storing tweets in a list after removing user mentions and hashtags
xl = pd.read_excel("tweets_Nov_2017.xlsx")
tweets = []
anewValence = []
anewValenceMean = []
wordCountsForValence = 0
wordCountMatch = []
wordCounts = []

for i in range(0, xl['Tweet Text'].size):
    wordCountsForValence = 0
    tweet = emoji_pattern.sub(r'', xl['Tweet Text'][i])
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)"," ",tweet).split())
    tweets.append(tweet.lower())
    words = tweet.split()
    val = 0
    length = len(words)
    
    for j in range(0,len(words)):
        if words[j].lower() in anewDict:
            wordCountsForValence = wordCountsForValence + 1
            val += float(anewDict.get(words[j].lower()))
    if wordCountsForValence > 0:
        anewValenceMean.append(val/wordCountsForValence)
        wordCountMatch.append(wordCountsForValence)
    else:
        anewValenceMean.append(-1)
        wordCountMatch.append(-1)
        
    anewValence.append(val)
    wordCounts.append(length)

nrc = pd.read_excel("Data/NRC-Emotion-Lexicon-v0.92-InManyLanguages-web.xlsx")

nrc = nrc[['English Word', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']]

#Calculating sentiment and emotion scores for each tweet
NRCEmotionLexicon = []
for i in range(0, len(tweets)):
    temp = np.zeros(10,)  
    tweet = tweets[i]
    words = tweet.split()
    for w in words:
        if nrc['English Word'].isin([w]).any():
            vec = np.delete(nrc[nrc['English Word'] == w].values,0)
            temp = np.add(temp, vec)
    NRCEmotionLexicon.append(temp.tolist())

concreteness = pd.read_csv("Data/concreteness.txt",sep="	")
concretenessDict = dict()

for i in range(0,concreteness['Word'].size):
    concretenessDict[concreteness['Word'][i]] = concreteness['Conc.M'][i]

#Calculating concreteness of each tweet
concreteTweetScores = []
for i in range(0, len(tweets)):
    tweet = tweets[i]
    words = tweet.split()
    concreteScore = 0
    for w in words:
        if w.lower() in concretenessDict:
            concreteScore = concreteScore + concretenessDict.get(w.lower())
    concreteTweetScores.append(concreteScore)

#Calculating polarity of each tweet
polarity = []
for i in range(0, len(tweets)):
    tempTweet = tweets[i]
    tempTweet = TextBlob(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tempTweet).split()))
    polarity.append(tempTweet.sentiment.polarity)

test = pd.concat([xl['Tweet Text'],pd.DataFrame(tweets),pd.DataFrame(anewValence),pd.DataFrame(anewValenceMean),pd.DataFrame(wordCountMatch),pd.DataFrame(polarity), pd.DataFrame(NRCEmotionLexicon), pd.DataFrame(wordCounts), pd.DataFrame(concreteTweetScores)], axis = 1)
test.columns = ["Tweet text","Modified Tweet Text", "Valence Score", "Valence Score Mean", "Word Count Match", "Polarity", 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust', "Word Count","concreteness"]
test.to_csv('tweets_Nov_2017_Evaluation.csv')

nouns = []
i = 0
for i in range(0,len(tweets)):
    tokens = nltk.word_tokenize(tweets[i])
    tagged = nltk.pos_tag(tokens)
    noun = [item[0] for item in tagged if item[1][0] == 'N']
    nouns.append(noun)
