import urllib
from bs4 import BeautifulSoup
import requests
import os


# class for scrap data from wikiart
class ScrapData:

    """This class scrap pictures from urls"""
    def __init__(self):

        # initializer
        self.is_directory = None
        self.directory_name = None
        self.painters_names = ["salvador-dali", "leonardo-da-vinci", "vincet-van-gogh",
                               "claude-monet", "pablo-picasso", "sandro-botticelli",
                               "henri-matisse", "raphael", "frida-kahlo",
                               "paul-cezanne", "michelangelo"]
        self.current_painter = None
        self.base_url = "https://www.wikiart.org/en/{}/all-works/text-list"
        self.main_url = "https://www.wikiart.org"

    # get request to page
    def get_requests(self, painter: str, url: str):

        """this method request the url and returns the content of the page"""
        self.current_painter = painter

        # requests
        request = requests.get(url)

        # status code control
        if request.status_code != 200:
            print("--EXCEPTİON--")
            return None

        print("status code approved")
        return request.content

    # scrap the all lists href
    def scrap_hrefs(self, content):
        """This method returns the hrefs of page"""
        soup = BeautifulSoup(content, "lxml")

        all_hrefs = soup.select(".painting-list-text-row a")
        href_list = []

        for href in all_hrefs:
            href_list.append(self.main_url+href["href"])
        return href_list

    def main_scraping(self):

        """all methods conceited in this method"""
        for painter in self.painters_names:
            url = self.base_url.format(painter)
            content = self.get_requests(painter=painter, url=url)
            links = self.scrap_hrefs(content=content)
            print(links)
            break


c = ScrapData()
c.main_scraping()



