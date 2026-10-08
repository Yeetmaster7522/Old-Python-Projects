#imports
import praw
import json
import pprint

#info
client_id = ""
client_secret = ""
user_agent = "FridayV3"

#model
reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent = user_agent
)

#make sure it only reads reddit data
print(reddit.read_only)


#search for top posts in a subreddit
subreddit = reddit.subreddit("minecraft")

post_list = []

for post in subreddit.top(limit=50):
    post_list.append(
        {
            "title": post.title,
            "score": post.score,
            "ID": post.id,
            "reply": post.reply,
            "URL": post.url
        }
    )
    print(f"Title: {post.title}, Score: {post.score}, ID: {post.id}, URL: {post.url}, reply: {post.reply}")

for post in post_list:
    print(post["title"])
    
    try:
        submission = reddit.submission(post["URL"])
        submission.comment_sort = "new"
        top_level_comments = list(submission.comments)
        all_comments = submission.comments.list()

        pprint(all_comments)
    except Exception as e:
        print(e)