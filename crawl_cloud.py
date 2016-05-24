#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from wordcloud import WordCloud
import operator
import re
import time
import praw

# Login to reddit.
import login
r = login.login()

# Define words to match in an array.
avoid = ["[", "]"]
# List to hold links.
links = []
# A cache for comments that have already been responded to.
cache = []
# Dictionary to measure word counts.  Defaultdict lets us skip checking (does it for us).
dictcount = defaultdict(int)
# Log to write to.
#log = open("./log")

# http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    parser = HTMLParser()
    html = parser.unescape(html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def sortdict(d):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_d

def bad(word):
    if bool(a.search(word)):
        return True
    return False

l = re.compile("http.*?[^ \)]*")
s = re.compile("\[.*?\]\]*")
a = re.compile("[^a-z ]+")
def run_bot():
    # Count duplicate posts.
    duplicate = 0

    # Get top 30 posts from all.
    subreddit = r.get_subreddit("all")
    submissions = subreddit.get_hot(limit=1)

    # For each post, put the id in a cache and then scan it.
    for submission in submissions:
        print("Getting submission, submission id: " + submission.id + "...")
        if submission.id in cache:
            # Count duplicates, alternatively just use parse here.
            # TODO, heat up when there is less duplicates each time?
            duplicate += 1
        else:
            # Now it has been read, send to cache.
            cache.append(submission.id)
            # All comments.
            submission.replace_more_comments(limit=None, threshold=0)
            # Flatten the comment tree, we don't care.
            flat = praw.helpers.flatten_tree(submission.comments)

            # For each comment in the flat tree.
            print("Submission got, scanning.")
            for comment in flat:
                #print (strip_tags(comment.body))
                comment = str(comment.body)
                # Get the links before we destroy everything...
                if l.search(comment):
                    links.append(l.search(comment).group())
                    # Try to remove link.
                    comment = l.sub("", comment)

                comment = comment.lower()
                # Try to strip out things between [].
                comment = s.sub("", comment)
                # Strip out anything else (anything other than words).
                #comment = a.sub("", comment)

                # Iterate over the words.
                for word in comment.split():
                    # Count the word, count it.
                    if bad(word) == False:
                        dictcount[word] += 1

    print("Duplicate posts this scan: " + str(duplicate))

runs = 1
while True:
    run_bot() # Run the bot!
    newstr = ""
    for x in dictcount:
        newstr = newstr + ((x + " ") * dictcount[x])

    wordcloud = WordCloud().generate(newstr)
    image = wordcloud.to_image()
    image.show()
    for whatever in sortdict(dictcount):
        print(whatever)
    print("Number of scans: " + str(runs))
    time.sleep(200) # Not too often…
    runs += 1

#log.close()
