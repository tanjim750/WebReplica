import re,os
from replicator.__request import ManageRequest


manage_request = ManageRequest()

class Replicator:
    def __init__(self,url):
        self.url = url
        self.pages = [self.url]
        self.css = []
        self.js = []
        self.files = []
        self.visited_pages = []

    def clonePage(self):
        current_page = self.pages.pop()
        self.visited_pages.append(current_page)

        html, pages, css, js, files = manage_request.start(current_page)
        self.pages.extend(page for page in pages if page not in self.pages and page not in self.visited_pages)
        self.css.extend(c for c in css if c not in self.css)
        self.js.extend(j for j in js if j not in self.js)
        self.files.extend(file for file in files if file not in self.files)

        if len(self.pages) != 0:
            self.clonePage()
        