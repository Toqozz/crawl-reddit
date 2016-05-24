from io import BytesIO
import sys
import re
import json
import pycurl
import index




#from collections import namedtuple
def parse():
    #search_terms = namedtuple("Terms", 'title')
    st = []

    for argument in sys.argv[1:]:
        if argument.startswith("t:"):
            st.append(re.compile(argument[2:]))
        else:
            print("wtf am i reading, use arguments properly.")
            sys.exit()

    return st

def fetch_raw():
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, "https://www.reddit.com/r/talesfromtechsupport.json")
    curl.setopt(curl.USERAGENT, "/u/Toqoz")
    curl.setopt(curl.WRITEDATA, buffer)
    #curl.setopt(curl.VERBOSE, True)
    curl.perform()
    curl.close()

    return buffer.getvalue().decode('utf-8')

def fetch_titles(body):
    titles = []
    number_of_posts = len(json.loads(body)["data"]["children"])
    for i in range(number_of_posts):
        response = json.loads(body)["data"]["children"][i]["data"]
        titles.append(response["title"])

    return titles

cache = []
def scan(titles, search_terms):
    # Count duplicate posts.
    duplicate = 0

    # For each post, put the id in a cache and then scan it.
    for title in titles:
        #print("Scanning submission, submission id: " + "fake" + "...")

        for expression in search_terms:
            if expression.search(title):
                pass

    print("Duplicate posts this scan: " + str(duplicate))

def main():
    st = parse()
    print (st)

    data = fetch_raw()
    titles = fetch_titles(data)
    index.beautify(titles)
    scan(titles, st)

if __name__ == "__main__":
    main()

