import requests
import bs4
import dateutil.parser

def main():
    response = requests.get("https://download.nvidia.com/opensuse/tumbleweed/x86_64/")
    page = bs4.BeautifulSoup(response.content, "lxml")
    dates = [elem.text for elem in page.select("span.date")]
    dates = [dateutil.parser.parse(text) for text in dates]
    print(max(dates))


if __name__ == "__main__":
    main()

