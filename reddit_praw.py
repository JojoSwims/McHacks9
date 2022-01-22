import praw
import pandas as pd
from praw.models import MoreComments
from sentiment_analysis import *

CLIENT_ID = "lI09GgRKEUoInMb13yXFig"
SECRET_KEY = "Wff8cfbOm2U-fMArXsPAnxgKnhuvJw"
MIN_NUMBER_COMMENTS = 100

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET_KEY, password='MGV2vag6nkg7cvb*nzp',
                     user_agent='MyAPI/0.0.1', username='BodaciousBelugas')


def get_good_comments(post):
    # post.replace_more_comments(limit=None, threshold=0)
    comments = []
    for comment in post.comments:
        if isinstance(comment, MoreComments):
            continue
        if len(comment.body) >= 12:
            comments.append((comment.ups, com_sentiment(comment.body)))

    return comments


def get_posts(url):
    posts = reddit.subreddit("all").search("url:"+url)
    ending_list = []
    for post in posts:
        subreddit = post.subreddit
        if len(get_good_comments(post)) < MIN_NUMBER_COMMENTS:
            continue
        ending_list.append(
            (subreddit, post.ups, get_good_comments(post)))
    return ending_list


def get_unique_sub_list(list_of_posts):
    unique_sub = {}
    for post in list_of_posts:
        if post[0] in unique_sub:
            unique_sub[post[0]] = (
                unique_sub[post[0]][0] + post[1], unique_sub[post[0]][1]+post[2])

        else:
            unique_sub[post[0]] = (post[1], post[2])
    return unique_sub


def get_ratio(unique_subs):
    ratios = []
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
        ratios.append((pondered_pos, pondered_neg, neu))
    return ratios


posts = get_posts(
    "https://www.theglobeandmail.com/opinion/article-the-american-polity-is-cracked-and-might-collapse-canada-must-prepare/")

unique_subreddits = get_unique_sub_list(posts)

print(unique_subreddits)
