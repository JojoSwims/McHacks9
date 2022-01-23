import praw
import pandas as pd
from praw.models import MoreComments
from sentiment_analysis import *

# Access to API do not change
CLIENT_ID = "lI09GgRKEUoInMb13yXFig"
SECRET_KEY = "Wff8cfbOm2U-fMArXsPAnxgKnhuvJw"
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET_KEY, password='MGV2vag6nkg7cvb*nzp',
                     user_agent='MyAPI/0.0.1', username='BodaciousBelugas')

# used in get_posts function
MIN_NUMBER_COMMENTS = 100

# returns a list of tuples, each tuple representing a comment. The tules are of the form (number of upvotes, sentiment of comment)


def get_good_comments(post):
    comments = []
    for comment in post.comments:
        # Weird thing about library but needed for the function to work
        if isinstance(comment, MoreComments):
            continue
        # remove comments of less than 12 characters to remove useless comments for the sentiment analysis
        if len(comment.body) >= 12:
            comments.append((comment.ups, com_sentiment(comment.body)))

    return comments


# getting all posts that have the url of the article in it
def get_posts(url):
    posts = reddit.subreddit("all").search("url:"+url)
    list_of_posts = []
    for post in posts:
        subreddit = post.subreddit
        if len(get_good_comments(post)) < MIN_NUMBER_COMMENTS:
            continue
        list_of_posts.append(
            (subreddit, post.ups, get_good_comments(post)))
    return list_of_posts


def get_unique_sub_list(list_of_posts):
    unique_subs = {}
    for post in list_of_posts:
        if post[0] in unique_subs:
            unique_subs[post[0]] = (
                unique_subs[post[0]][0] + post[1], unique_subs[post[0]][1]+post[2])

        else:
            unique_subs[post[0]] = (post[1], post[2])
    return unique_subs


def get_percentage(unique_subs):

    percentage_dict = {}
    for sub in unique_subs:
        pondered_pos = 0
        pondered_neg = 0
        neu = 0
        for com in unique_subs[sub][1]:
            if com[1] == "pos":
                pondered_pos += 1
            elif com[1] == "neg":
                pondered_neg += 1
            else:
                neu += 1

        percentage_dict[sub] = pondered_pos/(pondered_pos+pondered_neg)
    return percentage_dict


def get_final_dictionnary(list_of_articles):
    posts_from_all_articles = []
    for article in list_of_articles:
        posts_from_all_articles.append(get_posts(article[2]))
    unique_sub_list = get_unique_sub_list(posts_from_all_articles)
    percentage_dict = get_percentage(unique_sub_list)

    return percentage_dict


posts = get_posts(
    "https://www.theglobeandmail.com/opinion/article-the-american-polity-is-cracked-and-might-collapse-canada-must-prepare/")

unique_subreddits = get_unique_sub_list(posts)

print(unique_subreddits)
