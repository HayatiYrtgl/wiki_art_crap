import urllib.request
from bs4 import BeautifulSoup
import requests
import os


# class for scrap data from wikiart
class ScrapData:

    """This class scrap pictures from urls"""
    def __init__(self):

        # initializer
        self.painters_names = ["salvador-dali", "leonardo-da-vinci", "vincent-van-gogh",
                               "claude-monet", "pablo-picasso", "sandro-botticelli",
                               "henri-matisse", "raphael", "frida-kahlo",
                               "paul-cezanne", "michelangelo"]
        self.current_painter = None
        self.base_url = "https://www.wikiart.org/en/{}/all-works/text-list"
        self.main_url = "https://www.wikiart.org"
        self.all_painting_links = []


    # get request to page
    def get_requests(self, painter: str, url: str):

        """this method request the url and returns the content of the page"""
        self.current_painter = painter

        # requests
        request = requests.get(url)

        # status code control
        if request.status_code != 200:
            print(request.status_code)
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

    # scrape images
    @staticmethod
    def scrap_image_href(content):
        """this method scraps iamge href"""
        soup = BeautifulSoup(content, "lxml")
        image = soup.select_one(".btn-overlay-wrapper-artwork img")
        return image["src"]

    # download image
    def download_image(self, url: str, painter: str, file_name: int):
        # control
        self.control_directory(painter)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, f"paintings/{painter}/{file_name}.png")


    # control the director
    @staticmethod
    def control_directory(dir_name):
        if os.path.exists(f"paintings/{dir_name}"):
            pass
        else:
            os.mkdir(f"paintings/{dir_name}")
            print("Path is Created")

    def main_scraping(self):
        num = 0
        """all methods conceited in this method"""
        # get all paintings
        for painter in self.painters_names:
            url = self.base_url.format(painter)
            content = self.get_requests(painter=painter, url=url)
            links = self.scrap_hrefs(content=content)
            self.all_painting_links.append((painter, links))

        # download
        for painter, url_list in self.all_painting_links:
            for url in url_list:
                content = self.get_requests(url=url, painter=painter)
                image_src = self.scrap_image_href(content=content)
                self.download_image(url=image_src, painter=painter, file_name=num)
                print("başarılı")
                num += 1


c = ScrapData()
c.main_scraping()



