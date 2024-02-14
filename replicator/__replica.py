import re,os
from replicator.__request import ManageRequest
from replicator.__output import SaveOutput

BASE_URL_PATTERN = r"(^(https?|ftp):\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
manage_request = ManageRequest()

class Replicator(SaveOutput):
    def __init__(self,url):
        self.url = url
        self.base_url = self.getBaseURL(url)
        self.pages = [self.url]
        self.css = []
        self.js = []
        self.files = []
        self.visited_pages = []

        self.output = SaveOutput(self.base_url)

    def getBaseURL(self,url):
        match = re.search(BASE_URL_PATTERN,url)
        return match.group(1) if match else None
    
    def clonePage(self):
        current_page = self.pages.pop()
        self.visited_pages.append(current_page)

        html, pages, css, js, files = manage_request.start(current_page,self.base_url)
        self.pages.extend(page for page in pages if page not in self.pages and page not in self.visited_pages)
        self.css.extend(c for c in css if c not in self.css)
        self.js.extend(j for j in js if j not in self.js)
        self.files.extend(file for file in files if file not in self.files)

        self.output.saveHtml(current_page,html,self.pages)
        print(self.output.html_files)
        if len(self.pages) != 0:
            self.clonePage()
        