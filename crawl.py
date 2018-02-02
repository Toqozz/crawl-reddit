#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import operator
import re
import time
import praw

# Login to reddit.
import login
r = login.login()

# A cache for comments that have already been responded to.
cache = []
# Log to write to.
#log = open("./log")


import collections
def parse():
    search_terms = collections.namedtuple("Terms", ['title', 'comments'])
    st = search_terms

    for argument in sys.argv[1:]:
        if argument.startswith("t:"):
            st.title = re.compile(argument[2:])
        elif argument.startswith("c:"):
            st.comments = re.compile(argument[2:])
        else:
            print("wtf am i reading, use arguments properly.")
            sys.exit()

    #print(st.title, st.comments)
    return st


def run_scan(match):
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
            print("Submission got, submission id: " + submission.id + "\n" + "Scanning...")
            for comment in flat:
                comment = str(comment.body).lower()
                #print (comment)
                if match.comments.match(comment):
                    print (comment)
                    print("found it!")

    print("Duplicate posts this scan: " + str(duplicate))

def make_index(data):
    html = open("index.html", "w")
    html.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>First heading</h1>\n<p>First paragraph.</p>\n</body>\n</html>")

    html.close()

def main():
    runs = 1
    search = parse()

    while True:
        run_scan(search)
        print("Number of scans: " + str(runs))
        time.sleep(200)
        runs += 1


if __name__ == "__main__":
    main()

#log.close()
