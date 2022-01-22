import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#This function returns the Sentiment of a reddit comment, either 'neg', 'neu' or 'pos'
def com_sentiment(com):
    sia = SentimentIntensityAnalyzer()
    sentiments=sia.polarity_scores(com)
    sentiments.pop('compound')
    return max(sentiments, key=sentiments.get)

