import requests
import re
from bs4 import BeautifulSoup

BASE_URL_PATTERN = r"(^(https?|ftp):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
# Define regular expression patterns for href and src links
HREF_PATTERN = re.compile(r'href=["\'](.*?)["\']')
SRC_PATTERN = re.compile(r'src=["\'](.*?)["\']')


class ManageRequest:
    def __init__(self,headers=None):

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
                return html_text
            else:
                return "invalid url. Try again with a valid url"
        except:
            return "Check your connection and try again."
    
    def parsePages(self,html):
        pages = HREF_PATTERN.findall(html)
        file_pattern = re.compile(r'[^/]+\.(?!html$)[^/.]+$')
        all_pages = []

        for page in pages:
            # page = page.get("href")

            if self.validURL(page) and page.startswith(self.base_url) and not bool(file_pattern.search(page)):
                if page not in all_pages:  all_pages.append(page)

            elif not self.validURL(page) and page.startswith("/") and not bool(file_pattern.search(page)):
                page = self.url+page
                if page not in all_pages:  all_pages.append(page)

        return all_pages
    
    def parseCss(self,html):
        css = HREF_PATTERN.findall(html)
        file_pattern = re.compile(r'[^/]+\.css$')
        all_css = []

        for css_ in css:
            # css_ = css_.get('href')

            if self.validURL(css_) and css_.startswith(self.base_url) and bool(file_pattern.search(css_)):
                if css_ not in all_css:  all_css.append(css_)

            elif not self.validURL(css_) and css_.startswith("/") and bool(file_pattern.search(css_)):
                css_ = self.url+css_
                if css_ not in all_css:  all_css.append(css_)

        return all_css

    def parseJs(self,html):
        js = SRC_PATTERN.findall(html)
        file_pattern = re.compile(r'[^/]+\.js$')
        all_js = []

        for js_ in js:
            if self.validURL(js_) and js_.startswith(self.base_url) and bool(file_pattern.search(js_)):
                if js_ not in all_js:  all_js.append(js_)

            elif not self.validURL(js_) and js_.startswith("/") and bool(file_pattern.search(js_)):
                js_ = self.url+js_
                if js_ not in all_js:  all_js.append(js_)

        return all_js

    def parseFiles(self,html,pages,css,js):
        href = HREF_PATTERN.findall(html)
        src = SRC_PATTERN.findall(html)
        file_pattern = re.compile(r'[^/]+\.(?!html$)[^/.]+$')
        all_files = []

        for h,s in zip(href,src):
            # add href links to self.others
            if self.validURL(h) and h.startswith(self.base_url):
                if h not in all_files and h not in pages and h not in css and h not in js: 
                    if bool(file_pattern.search(h)) :   all_files.append(h)
                    # else: pages.append(h)

            elif not self.validURL(h) and h.startswith("/"):
                h = self.url+h
                if h not in all_files and h not in pages and h not in css and h not in js:  
                    if bool(file_pattern.search(h)) :   all_files.append(h)
                    # else: self.pages.append(h)

            # add src links to all_files
            if self.validURL(s) and s.startswith(self.base_url):
                if s not in all_files and s not in pages and s not in css and s not in js:  
                    if bool(file_pattern.search(s)) :   all_files.append(s)
                    # else: self.pages.append(s)

            elif not self.validURL(s) and s.startswith("/"):
                s = self.url+s
                if s not in all_files and s not in pages and s not in css and s not in js:  
                    if bool(file_pattern.search(s)) :   all_files.append(s)
                    # else: self.pages.append(s)

        return all_files


    def start(self,url):
        self.url = url
        self.base_url = self.getBaseURL(url)

        html = self.parseHtml()
        pages = self.parsePages(html)
        css = self.parseCss(html)
        js = self.parseJs(html)
        files = self.parseFiles(html,pages,css,js)


        return html, pages, css, js, files
        
