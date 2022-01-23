from mediastack import get_articles
import praw
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

# returns a list of tuples, each tuple represents a post of the form (subreddit, upvotes, number of commnets, list of comments)
# getting all posts that have the url of the article in it
def get_posts(url):
    posts = reddit.subreddit("all").search("url:"+url)
    list_of_posts = []
    for post in posts:
        subreddit = post.subreddit
        list_of_posts.append(
            (subreddit, post.ups, post.num_comments, get_good_comments(post)))
    return list_of_posts


#PARTIALLY TESTED AND WORKS AS INTENDED
#Returns a list of tuples of the form (subreddit, upvotes, number of commnets, list of comments)
def get_list_of_posts(list_of_articles):
    posts_from_all_articles = []
    # list of articles is a list of tuples each representing an article, and each of the form (title, date, url)
    for article in list_of_articles:
        posts=get_posts(article[2])
        if(len(posts)>0):
            posts_from_all_articles+=(get_posts(article[2]))
    return posts_from_all_articles

def get_unique_subs(list_of_posts):
    unique_subs = {}
    for post in list_of_posts:
        # post is (subreddit, upvotes, list of comments)
        if post[0] in unique_subs:
            unique_subs[post[0]] = (
                unique_subs[post[0]][0] + post[1], unique_subs[post[0]][1]+post[2], unique_subs[post[0]][2]+post[3])

        else:
            unique_subs[post[0]] = (post[1], post[2], post[3])
    return unique_subs

def get_percentage(unique_subs):

    percentage_dict = {}
    for sub in unique_subs:
        pondered_pos = 0
        pondered_neg = 0
        total=0
        # unique_subs[sub] gives a tuple of the form (upvotes of posts, list of comments)
        # each comment if of the form (upvote, sentiment)
        for com in unique_subs[sub][2]:
            if com[1] == "pos":
                pondered_pos += 1
            elif com[1] == "neg":
                pondered_neg += 1
        total = pondered_pos+pondered_neg
        if(total>0):
            percentage_dict[sub.display_name] = (unique_subs[sub][0]+10*unique_subs[sub][1], pondered_pos/total, unique_subs[sub][0])
        else:
            percentage_dict[sub.display_name] = (unique_subs[sub][0]+10*unique_subs[sub][1], 'N/A', unique_subs[sub][0])
    return percentage_dict

def get_reactions_dic():
    all_posts=get_list_of_posts(get_articles())
    unique_subs=get_unique_subs(all_posts)
    return get_percentage(unique_subs)

