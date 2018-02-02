#!/usr/bin/env python3

from io import BytesIO
import sys
import re
import json
import pycurl

def parse():
    # Dictionary is the best suit that I can think of.
    # Where each key holds a list of regex matches.
    st = {"title": [], "comment": [], "url": ""}

    for argument in sys.argv[1:]:
        if argument.startswith("t:"):
            st["title"].append(re.compile(argument[2:]))
        elif argument.startswith("c:"):
            st["comment"].append(re.compile(argument[2:]))
        elif argument.startswith("u:"):
            st["url"] = argument[2:] + ".json"
        else:
            print("""usage: crawl_python [ t:[TITLE] | c:[COMMENTS] | u:[URL] ]

        TITLE:     String to search for in titles.
        COMMENTS:  String to search for in comments.
        URL:       The subreddit url to search on (i.e. https://www.reddit.com/r/all).

        Title / comment strings are regex supported, using python regex syntax.

        Example: crawl_curl t:[Aa]ustralia c:[dblgh]ota u:https://www.reddit.com/r/all

        Results are placed in an index.html file in the working directory.
        """)
            sys.exit()

    return st

def fetch_raw(url):
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.USERAGENT, "/u/Toqoz")
    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(pycurl.TIMEOUT, 20)
    #curl.setopt(curl.VERBOSE, True)
    curl.perform()
    curl.close()

    return buffer.getvalue().decode('utf-8')

cache = []
def fetch_data(body):
    duplicate = 0
    combo = {"titles": [], "comments": []}
    body = json.loads(body)

    # Titles <---.
    number_of_posts = len(body["data"]["children"])
    for i in range(number_of_posts):
        # Fetch the identity parameter from the json data.
        identity = body["data"]["children"][i]["data"]["id"]
        if identity in cache:
            duplicate += 1
        else:
            # Don't scan this one again.
            cache.append(identity)
            # Add all titles.
            response = body["data"]["children"][i]["data"]
            combo["titles"].append(response["title"])

        # We only know the url to fetch from about now.
        # I'm sure there is a better way, reusing the above code.
        url = "https://www.reddit.com" + response["permalink"] + ".json"
        print(url)
        body_comments = fetch_raw(url)
        body_comments = json.loads(body_comments)

        # Comments <---.
        number_of_comments = len(body_comments[1]["data"]["children"])
        for i in range(number_of_comments):
            # Identity again.
            identity = body_comments[1]["data"]["children"][i]["data"]["id"]
            if identity in cache:
                duplicate += 1
            # As long as the ccomment is a comment, it should be okay to scan.
            elif not body_comments[1]["data"]["children"][i]["kind"] == "more":
                # Sure hope comment ids don't cross over post ids…
                cache.append(identity)
                # Add all parents comments.
                response_comments = body_comments[1]["data"]["children"][i]["data"]
                combo["comments"].append(response_comments["body"])
                combo["comments"] += fetch_waterfall(response_comments)

    print("Duplicate posts this scan: " + str(duplicate))
    return combo

def fetch_waterfall(response):
    #print("go")
    waterfall = []
    if type(response["replies"]) == dict:
        number_of_responses = len(response["replies"]["data"]["children"])

        #try:
        for i in range(number_of_responses):
            if response["replies"]["data"]["children"][i]["kind"].startswith("t1"):
                #print(response["replies"]["data"]["children"][i]["data"]["body"])
                waterfall.append(response["replies"]["data"]["children"][i]["data"]["body"])
                response_new = response["replies"]["data"]["children"][i]["data"]
                waterfall += fetch_waterfall(response_new)
        #except:
            #pass

    return waterfall

def scan(combo, search_terms):
    # To hold matching things.
    matches = {"titles": [], "comments": []}

    # Check each title against the regex.
    for title in combo["titles"]:
        for expression in search_terms["title"]:
            if expression.search(title):
                matches["titles"].append(title)

    # Check each parent comment against the regex.
    for comment in combo["comments"]:
        for expression in search_terms["comment"]:
            #print(comment)
            if expression.search(comment):
                matches["comments"].append(comment)

    return matches

def beautify(data):
    # There has to be a better way to do this...
    buf = ""
    buf += "<!DOCTYPE html>\n"
    buf += "<html>\n"
    buf += "<body>\n"
    buf += "\n"
    buf += "<h1> These are the results! </h1>\n"
    buf += "\n"

    for item in data["titles"]:
        buf += "<p> Title: %s </p>\n" % item
    for item in data["comments"]:
        buf += "<p> Comment: %s </p>\n" % item

    buf += "\n"
    buf += "</body>\n"
    buf += "</html>"

    # Write to file, it wants to be overwritten.
    fo = open("index.html", "w")
    fo.write(buf)
    fo.close()

def main():
    st = parse()
    print (st)

    # Fetch raw data from reddit.
    data = fetch_raw(st["url"])
    # Get titles from the posts.
    combo = fetch_data(data)
    # Scan the titles for regex.
    matches = scan(combo, st)
    # Make a webpage index.html.
    beautify(matches)

if __name__ == "__main__":
    main()

