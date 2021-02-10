import json
import scrapy
from scrapy.crawler import CrawlerProcess
from os import system,name
result=None

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')
        
class ProfileSpider(scrapy.Spider):
    name="Profile"

    def __init__(self,username, name=name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.username=username
    def start_requests(self):
        urls = [
            f'https://github.com/{self.username}'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        global result
        clear()
        username=self.username
        try:
            pinnedRepositories=response.css("span.repo::text").getall()
            fullname=response.css("span.p-name.vcard-fullname.d-block.overflow-hidden::text").extract_first()
            following=int(response.css(".text-gray-dark:nth-child(1)::text").get())
            followers,stars=list(map(lambda i:int(i),response.css("span.text-gray-dark:nth-child(2)::text").getall()))
            description=response.css('div.p-note.user-profile-bio.mb-3.js-user-profile-bio.f4 div::text').get()
        except:
            pinnedRepositories=None
            fullname=None
            following=None
            followers,stars=None,None
            description=None
        clear()
        item = {
            "username":username,
            "fullname":fullname,
            "self_description":description,
            "pinned_repositories":pinnedRepositories,
            "following":following,
            "followers":followers,
            "stars":stars,
        }
        result=item
        yield item

 
def scrap_github_profile():
    process = CrawlerProcess()

    process.crawl(ProfileSpider,username=input("Enter the username to analyze: "))
    process.start()
    clear()
    print(result)
    with open("./result.json","a") as f:
        f.write(json.dumps(result))
    input("HIT ENTER TO EXIT")
