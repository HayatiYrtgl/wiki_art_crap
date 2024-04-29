import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup


class ScrapDataAsync:
    def __init__(self):
        self.painters_names = ["pyotr-konchalovsky"]
        self.base_url = "https://www.wikiart.org/en/{}/all-works/text-list"
        self.main_url = "https://www.wikiart.org"
        self.all_painting_links = []

    async def get_content(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_requests(self, painter, url, session):
        painter = painter
        content = await self.get_content(session, url)
        return content

    async def scrap_hrefs(self, content):
        soup = BeautifulSoup(content, "lxml")
        all_hrefs = soup.select(".painting-list-text-row a")
        href_list = [self.main_url + href["href"] for href in all_hrefs]
        return href_list

    @staticmethod
    async def scrap_image_href(content):
        soup = BeautifulSoup(content, "lxml")
        image = soup.select_one(".btn-overlay-wrapper-artwork img")
        return image["src"]

    async def download_image(self, url, painter, file_name, session):
        if not os.path.exists(f"paintings/{painter}"):
            os.makedirs(f"paintings/{painter}")

        async with session.get(url) as response:
            with open(f"paintings/{painter}/{file_name}.png", "wb") as f:
                f.write(await response.read())

    async def main_scraping(self):
        """This method contains all functions to scrap"""
        async with aiohttp.ClientSession() as session:
            for painter in self.painters_names:
                url = self.base_url.format(painter)
                content = await self.get_requests(painter, url, session)
                links = await self.scrap_hrefs(content)
                self.all_painting_links.append((painter, links))

            for painter, url_list in self.all_painting_links:
                for num, url in enumerate(url_list):
                    try:
                        content = await self.get_requests(url=url, painter=painter, session=session)
                        image_src = await self.scrap_image_href(content=content)
                        await self.download_image(url=image_src, painter=painter, file_name=num, session=session)
                        print("başarılı")
                    except:
                        print("başarisiz")



async def start_async_scraping():
    scrap_data = ScrapDataAsync()
    await scrap_data.main_scraping()


asyncio.run(start_async_scraping())
