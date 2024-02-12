import requests
import re
from bs4 import BeautifulSoup

BASE_URL_PATTERN = r"(^(https?|ftp):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"

class ManageRequest:
    def __init__(self,url,headers=None):
        self.url = self.getBaseURL(url)
        self.pages = []
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-length': '0',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            }

    def getBaseURL(self,url):
        match = re.search(BASE_URL_PATTERN,url)
        return match.group(1) if match else None
    
    def validURL(self,url):
        # Regular expression for a basic URL validation
        url_pattern = re.compile(
            r'^(https?|ftp):\/\/'  # http:// or https:// or ftp://
            r'(www\.)?'             # optional www
            r'[a-zA-Z0-9.-]+'       # domain name
            r'(\.[a-zA-Z]{2,})'     # dot-something
            r'(:\d{1,5})?'          # optional port
            r'([\/?#].*)?$'         # path, query parameters, or fragment
        )

        return bool(re.match(url_pattern, url))

    def parseHtml(self):
        try:
            response = requests.get(self.url, self.headers)
            if response.status_code == 200:
                html_text = response.text
                soup = BeautifulSoup(html_text, 'html_parser')
            else:
                return "invalid url. Try again with a valid url"
        except:
            return "Check your connection and try again."
    
    def parsePages(self,html_text):
        soup = BeautifulSoup(html_text, 'html_parser')
        pages = soup.find_all('a[href=""]')
        self.pages.extend(page for page in pages if page not in self.pages)
        for page in pages:
            page = str(page)

            if self.validURL(page) and page.startswith(self.url):
                self.pages.append(page)

            elif not self.validURL(page):
                page = self.url+page
                self.pages.append(page)
