import os,random

class SaveOutput:
    def __init__(self,base_url:str):
        self.base_url = base_url
        self.base_folder = self.baseFolder()
        self.html_files = {}

    def baseFolder(self):
        split_url = self.base_url.split('/')
        path = 'output/'+split_url[-1]
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    
    def uniqeFileName(self,page_url:str):
        page_url = page_url[:-1] if page_url.endswith('/') else page_url
        split_url = page_url.split('/')
        ends = split_url[-1]
        if ends.endswith('.html'):
            filename = ends
        else:
            filename = ends+".html"

        loop = filename in list(self.html_files.values())
        while loop:
            random_part = ''+str(random.randint(111,9999))
            filename = random_part+filename
            loop = filename in list(self.html_files.values())
        
        return filename
    
    def saveHtml(self,current_page,html,html_pages):
        if len(self.html_files) == 0:
            filename = 'index.html'
        else:
            filename = self.uniqeFileName(current_page)
        self.html_files[current_page] = filename

        for page in html_pages:
            if page not in list(self.html_files.keys()):
                get_filename = self.uniqeFileName(page)
                self.html_files[page] = get_filename

        for k,v in self.html_files.items():
            k_ = k.replace(self.base_url,'') #without the base url
            k__ = k_.replace('/','',1) if k_.startswith('/') else k_ #without the starting slash(/)
            html = html.replace(k,v) if k.strip() != "" and k.strip() != "/" else html
            html = html.replace(k_,v) if k_.strip() != "" and k_.strip() != "/" else html
            html = html.replace(k__,v) if k__.strip() != "" and k__.strip() != "/" else html
        
        file_path = self.base_folder+"/"+filename
        with open(file_path,'w') as f:
            f.write(html)
        
        return file_path
        





