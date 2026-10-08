"""
https://old.reddit.com/prefs/apps/

It can extract data at a rate of 2 posts/min
Do not open database while running as it will crash the program or text editor
Only run on a good network to get fast rates

NOTES:
- Replies are given as an ID with a list value even though its storing 1 piece of data
- May require function to remove "[removed]" and "[deleted]" comments and replies (can be done with post-processing)
- Fix 429 HTTP response error
"""
#imports
import praw
import json
import time
import datetime
import os



#constants
reddit = praw.Reddit(
    client_id = "",
    client_secret = "",
    user_agent = ""
)

file_path = "neural networks\\language\\data.txt" #where the data will be stored



#functions
def handleCommentForest(submission) -> dict:
    """
    This handles comment forests by getting a list of comments within it and formatting them with their replies
    """
    
    converseDict = {}

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        commID = comment.id
        commBody = comment.body
        commParent = comment.parent()

        if comment.id not in converseDict:
            converseDict[commID] = [commBody, {}] #add comment
            if commParent != submission.id:
                converseDict[str(commParent)][1][commID] = [commBody] #add as reply

    return converseDict


def getSubmission(submission, data: list) -> dict:
    """
    Outputs details such as the title, ID, body, and comments given a submission.\n
    This requires existing data to be passed so that it will not output data that you already have.\n\n
    This will output [ ] if the submission is already in your data or it receives an error which it will print out.
    """

    try:
        title = submission.title
        ID = submission.id
        print(f"checking: {title}\n        ↪ {ID}\n") #debugging purposes (seeing what post is being processed)

        if ID not in [post["id"] for post in data]: #program will not add data that already exists
            output = {
                "id": ID,
                "title": title,
                "body": submission.selftext,
                "comments": handleCommentForest(submission)
            }
        else:
            output = [] #this makes program skip over it
    except Exception as e: #mainly used to overcome 429 HTTP response error
        print(e)
        output = [] #makes program skip over it
        time.sleep(30) #reduces chance of getting 429 HTTP response error twice in a row

    return output


def checkSubreddit(subredditName: str, limit: int, data: dict, delay: int):
    """
    Function to scrape data from subreddit
    """

    subR = reddit.subreddit(subredditName)

    for s in subR.top(limit=limit):
        submission = getSubmission(s, data)
        
        print(f"time: {datetime.datetime.now()}")
        print(f"posts in data: {len(data)}")
        print(f"file size: {os.path.getsize(file_path)/1000000000} GB\n")

        if submission: #will not add data that is already there or if there was an error
            data.append(submission)
            
            print("DO NOT CLOSE NOW") #useful for shutting down program safely and not corrupting file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            print("YOU MAY CLOSE NOW\n")

            time.sleep(delay)

    print(f"-------------------------\nDONE CHECKING {subredditName}\n-------------------------\n")



#load up data and scan subreddits
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"posts in data: {len(data)}\n")

    for subreddit in ["worldnews", "cubers", "gundam", "gunpla"]: #do r/askReddit sometime when fix 429 HTTP response error
        checkSubreddit(subreddit, limit=1000, data=data, delay=20)
        time.sleep(10)