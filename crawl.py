#! /usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import time
import login

# Login to reddit.
r = login.login()

# Define words to match in an array.
words_to_match = ["i"]
# A cache for comments that have already been responded to.
cache = []
# Log to write to.
#log = open("./log")


def run_bot():
    # Count duplicate posts.
    duplicate = 0

    subreddit = r.get_subreddit("all")
    posts = subreddit.get_hot(limit=100)

    for post in posts:
        if post.id in cache:
            duplicate += 1
        else:
            cache.append(post.id)
            for item in words_to_match:
                if item in post.title:
                    print("found one: " + post.title)
    print("Duplicate posts this scan: " + str(duplicate))
    duplicate = 0

runs = 1
while True:
    run_bot() # Run the bot!
    time.sleep(10) # Not too often…
    print("Number of scans: " + str(runs))
    runs += 1
