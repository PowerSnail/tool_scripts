#!/usr/bin/env python3

import requests
import bs4
import sys
import subprocess as sp


URL = "https://review.tumbleweed.boombatower.com/"


def parse_item(tag):
    stability = tag.select_one(".release-stability-level").text.strip()
    date = tag.select_one("h3 a").text.strip()
    date = date.replace("-", "")
    return date, stability


def main():
    content = requests.get(URL).content
    page = bs4.BeautifulSoup(content, "lxml")
    item_list = [parse_item(li) for li in page.select(".post-list>li")]
    latest_stable = max(filter(lambda item: item[1] == "stable", item_list))[0]
    sp.run(["tumbleweed", "status"])
    print(f"stable   : {latest_stable}")



if __name__ == "__main__":
    main()
