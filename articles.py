import reddit_praw


class Article:
    def __init__(self, art_descr):
        self.title = art_descr[0]
        self.date = art_descr[1]
        self.url = art_descr[2]

    def get_posts(self):
        self.posts = reddit_praw.get_posts(self.url)


class Event:
    def __init__(self, query_title):
        self.query_title = query_title

    def get_articles(self):
        self.articles = []  # needs to be done by alex

    def get_reddit_posts(self):
        for article in self.articles:
            res = reddit.subreddit("all").search("url:"+article[2])
            posts_one_news = pd.DataFrame()
            for post in res:
                posts_one_news = posts_one_news.append({
                    'post_id': post.id,
                    'title': post.title,
                    # 'link' : 'reddit.com' + post.permalink,
                    'subreddit': post.subreddit,
                    'upvotes': post.ups
                }, ignore_index=True)

        self.reddit_posts = posts_one_news
