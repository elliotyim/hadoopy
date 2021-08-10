import json
from typing import List

import printer

import requests
from bs4 import BeautifulSoup

NAVER_BLOG = "https://blog.naver.com"
BLOG_SECTION = "https://section.blog.naver.com"

API_URL = BLOG_SECTION + "/ajax/SearchList.nhn"
HEADERS = {"Referer": BLOG_SECTION}
PARAMS = {"countPerPage": 30}


def fetch_blogs() -> List[str]:
    """
    Get blogs from api as the searching page is dynamically rendered.
    For some reason, response data contain 6 unnecessary characters.
    Slice the list to remove them.
    """
    response = requests.get(API_URL, headers=HEADERS, params=PARAMS).text[6:]
    response_data = json.loads(response)
    return response_data["result"]["searchList"]


def parse(url: str) -> BeautifulSoup:
    """
    Return a BeautifulSoup object which contains parsed html tags.
    """
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")


def get_blogs() -> None:
    """
    Fetch blog texts and print them into a txt file.
    """
    blogs = fetch_blogs()
    post_urls = [blog["postUrl"] for blog in blogs]

    # Crawl the urls to get the blog contents.
    contents: List[str] = []
    for (i, url) in enumerate(post_urls):
        print(f"{len(post_urls)}/{i + 1}")
        try:
            if "blog.me" in url:
                url = f"{NAVER_BLOG}/{blogs[i]['blogId']}/{blogs[i]['logNo']}"

            # Extract the real contents from iframes.
            src = parse(url).find("iframe", id="mainFrame")["src"]
            main_content = parse(NAVER_BLOG + src).select("div.se-main-container")[0]

            content = main_content.text.replace("\n", "").strip()
            contents.append(f"title: {blogs[i]['noTagTitle']}\ncontent: " + content)
        except Exception:
            print(f"An error occured with url: {url}")
    return contents


if __name__ == "__main__":
    PARAMS["keyword"] = input("Enter a keyword.\n> ")
    print("Processing...")
    blogs = get_blogs()
    printer.print(directory="../crawling_result", contents=blogs)
    print("Done.")
