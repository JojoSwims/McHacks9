from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# This function returns the Sentiment of a reddit comment, either 'neg', 'neu' or 'pos'


def com_sentiment(com):
    sia = SentimentIntensityAnalyzer()
    sentiments = sia.polarity_scores(com)
    sentiments.pop('compound')
    if(sentiments['pos'] > 0 and sentiments['pos'] > sentiments['neg']):
        return 'pos'
    elif (sentiments['neg'] > 0 and sentiments['neg'] > sentiments['pos']):
        return 'neg'
    else:
        return 'neu'
