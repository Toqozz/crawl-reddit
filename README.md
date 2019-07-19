# crawl

Crawl is reddit post crawler that finds keyword text in post titles and comments.

For instance, one can search for the string "Australia" in post titles, and posts in the targeted subreddit containing "Australia" will be returned.  The behavior is similar for comments.

## versions

There are two versions of crawl in this repository.  One version uses the Reddit praw API, and the other uses pycurl to scrape directly from the website.

The benefit to the curl approach is that it doesn't require an OAuth module, and it's generally a little bit faster.

I recommend generally sticking to `crawl_curl.py`.

## dependencies

If using regular `crawl`, you'll need to install `praw`: `pip install --user praw`.

If using `crawl_curl` (recommended), you'll need to install `pycurl`: `pip install --user pycurl`.

If these are available in your distro's repositories, please install them using your package manager rather than pip.

## usage

From `crawl_curl help`:
```
usage: crawl_python [ t:[TITLE] | c:[COMMENTS] | u:[URL] ]

        TITLE:     String to search for in titles.
        COMMENTS:  String to search for in comments.
        URL:       The subreddit url to search on (i.e. https://www.reddit.com/r/all).

        Title / comment strings are regex supported, using python regex syntax.

        Example: crawl_curl t:[Aa]ustralia c:[dblgh]ota u:https://www.reddit.com/r/all

        Results are placed in an index.html file in the working directory.
```

The reasoning behind putting results in a html file rather than plain text was because of the program use case at the time it was made.  A html file was easier to host online, and then download and parse through an app or something like that.

## improvements
* Add an option for the refresh time.
* Add an option to output results to plain text.
* Clean up syntax.
