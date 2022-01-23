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
MIN_NUMBER_COMMENTS = 0

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


# returns a list of tuples, each tuple represents a post of the form (subreddit, upvotes, list of comments)
# getting all posts that have the url of the article in it
def get_posts(url):
    posts = reddit.subreddit("all").search("url:"+url)
    list_of_posts = []
    for post in posts:
        subreddit = post.subreddit
        # if want more comments, lower the min number of comments constants
        if len(get_good_comments(post)) < MIN_NUMBER_COMMENTS:
            continue

        list_of_posts.append(
            (subreddit, post.ups, get_good_comments(post)))
    return list_of_posts


# In list of posts we can have multiple posts for each subreddit, with this function we return a dictionnary with
# keys being subredits, and value a tuple of the form ( upvotes of all posts from this subreddit added, list of all comments from all posts from this subreddit
def get_unique_sub_list(list_of_posts):
    unique_subs = {}
    for post in list_of_posts:
        # post is (subreddit, upvotes, list of comments)
        if post[0] in unique_subs:
            unique_subs[post[0]] = (
                unique_subs[post[0]][0] + post[1], unique_subs[post[0]][1]+post[2])

        else:
            unique_subs[post[0]] = (post[1], post[2])
    return unique_subs


# returns a dictionary with keys being subreddits and values being percentage of positive comments from the posts we got
def get_percentage(unique_subs):

    percentage_dict = {}
    do_not_div_by_zero = 1
    for sub in unique_subs:
        pondered_pos = 0
        pondered_neg = 0
        # unique_subs[sub] gives a tuple of the form (upvotes of posts, list of comments)
        # each comment if of the form (upvote, sentiment)
        for com in unique_subs[sub][1]:
            if com[1] == "pos":
                pondered_pos += 1
            elif com[1] == "neg":
                pondered_neg += 1
        if pondered_pos+pondered_neg != 0:
            do_not_div_by_zero = pondered_pos+pondered_neg
        percentage_dict[sub] = (
            pondered_pos/do_not_div_by_zero, unique_subs[sub][0])
    return percentage_dict


def get_final_dictionnary(list_of_articles):
    posts_from_all_articles = []
    # list of articles is a list of tuples each representing an article, and each of the form (title, date, url)
    for article in list_of_articles:
        posts_from_all_articles.append(get_posts(article[2]))
    unique_sub_list = get_unique_sub_list(posts_from_all_articles)
    percentage_dict = get_percentage(unique_sub_list)

    return percentage_dict


# Tests
posts = get_posts(
    "https://www.theglobeandmail.com/opinion/article-the-american-polity-is-cracked-and-might-collapse-canada-must-prepare/")

unique_subreddits = get_unique_sub_list(posts)

print(get_percentage(unique_subreddits))
