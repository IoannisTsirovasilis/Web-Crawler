from bs4 import BeautifulSoup
import requests
import re
import time

starting_node = "https://moz.com/top500"
crawled = []
to_be_crawled_list = [starting_node]
reg_exp = re.compile("https?://(www[.])?[-\w]+[.](org|com|net|int|edu|gov|mil|gr)/?$")


def crawl(to_be_crawled, max):
    print("List with crawled sites: {0}".format(crawled))
    print("List to be crawled: {0}".format(to_be_crawled))
    if len(to_be_crawled) == 0 or len(crawled) >= max:
        return
    else:
        for url in to_be_crawled[:]:
            if url in crawled:
                to_be_crawled.remove(url)
                continue
            print("Site currently crawling: {0}".format(url))
            try:
                print("Requesting HTML code...")
                text = requests.get(url).text
                soup = BeautifulSoup(text, "html.parser")
            except:
                print("Error on fetching HTML code. Site is assumed to have been crawled.")
                crawled.append(url)
                to_be_crawled.remove(url)
                continue
            print("HTML code successfully fetched!")
            print("Fetching all <a> tags...")
            a_tags = soup.find_all("a")
            print("Checking each href attribute...")
            for link in a_tags:
                tmp = str(link.get("href"))
                tmp = tmp.replace('www.', '')
                print("Href currently checking: {0}".format(tmp))
                if tmp in to_be_crawled or tmp in crawled:
                    continue
                if reg_exp.match(tmp):
                    print("Adding in the list with to be crawled urls: {0}".format(tmp))
                    to_be_crawled.append(tmp)
            print("Crawl ended. Removing '{0}' from to be crawled list.".format(url))
            to_be_crawled.remove(url)
            print("Adding  '{0}' to crawled list.".format(url))
            crawled.append(url)
            with open("C:\\Users\\Giannis\\Desktop\\w_b.txt", "a") as f:
                print("Writing '{0}' to the file with crawled urls.".format(url))
                f.write(url)
                f.write("\n")
            if len(crawled) >= max:
                return
        crawl(to_be_crawled, max)


def print_sleep(message, seconds=1):
    print(message)
    time.sleep(seconds)


def main():
    max = 100
    print("Starting crawling...")
    print("Entry site: {0}".format(starting_node))
    crawl(to_be_crawled_list, max)


if __name__ == "__main__":
    main()
