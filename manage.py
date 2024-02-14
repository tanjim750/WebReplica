from colorama import Fore, Style
import os
import re

from replicator.__request import ManageRequest

def extract_domain(url):
    match = re.search(r'https?://(?:www\.)?([a-zA-Z0-9.-]+)', url)
    return match.group(1) if match else None

def validate_url(url):
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

def input_text(text=None,color=None):
    if text is None:
        text_ = Fore.RED+"\n╔═══"+Fore.CYAN+"["+Fore.GREEN+"Tanjim"+Fore.CYAN+"]"+Fore.RED+"══════"+Fore.CYAN+"["+Fore.GREEN+"HuntApi"+Fore.CYAN+"]"+"\n"+Fore.RED+"║"+"\n"+Fore.RED+"╚═══➣➣ "+Fore.GREEN
    else:
        text_ = Fore.RED+"\n╔═══"+Fore.CYAN+"["+color+text+Fore.CYAN+"]"+"\n"+Fore.RED+"║"+"\n"+Fore.RED+"╚═══➣➣ "+Fore.GREEN
    return text_

os.mkfifo('output/file.html')
web_url = input(input_text("Enter your target Web URL(with 'http or https')",Fore.GREEN))
if not validate_url(web_url): # if domain can be extracted then the url is valid
    web_url = ""

while len(web_url) < 1:
    web_url = input(input_text('Enter a valid Web URL(with "http or https")',Fore.RED))
    if not validate_url(web_url): # if domain can be extracted then the url is valid
        web_url = ""

manage_request = ManageRequest(web_url)
html, pages, css, js, files = manage_request.start()

print("All Pages:",pages,"\n\n\nAll Js files:", js, "\n\n\nAll css files:",css,"\n\n\nAll others link:",files)