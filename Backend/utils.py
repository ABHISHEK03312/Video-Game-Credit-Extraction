from linkedin_scraper import Person, actions
from selenium import webdriver
import random
import argparse
import requests
import re
# from fake_useragent import UserAgent
import time

class LinkedinScraper(object):
    def __init__(self, keyword, limit):
        """
        :param keyword: a str of keyword(s) to search for
        :param limit: number of profiles to scrape
        """
        self.keyword = keyword.replace(' ', '%20')
        self.all_htmls = ""
        self.quantity = '10'
        self.limit = int(limit)
        self.counter = 0
    
    def search(self):
    
    
        # choose a random user agent
        # try:
        #     ua = UserAgent()
        # except FakeUserAgentError:
        #     ua=None
        user_agents = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/11.10 Chromium/18.0.1025.142 Chrome/18.0.1025.142 Safari/535.19',
            'Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00'
        ]
        while self.counter < self.limit:
            # if ua==None:
            headers = {'User-Agent': random.choice(user_agents)}
            # else:
            # headers = {'User-Agent': ua.random}
            time.sleep(2)
            url = 'http://google.com/search?num=100&start=' + str(self.counter) + '&hl=en&meta=&q=site%3Alinkedin.com/in%20' + self.keyword
            resp = requests.get(url, headers=headers)
            if ("Our systems have detected unusual traffic from your computer network.") in resp.text:
                print("Running into captchas")
                return
        
            self.all_htmls += resp.text
            self.counter += 5

    def parse_links(self):
        reg_links = re.compile(r"url=https:\/\/*[a-z]+\.linkedin.com(.*?)&")
        # print(self.all_htmls)
        self.temp = reg_links.findall(self.all_htmls)
        # print (self.temp)
        results = []
        for regex in self.temp:
            final_url = regex.replace("url=", "")
            # print (final_url)
            results.append("https://www.linkedin.com" + final_url)
        return results
    

    def parse_people(self):
        """
        :param html: parse the html for Linkedin Profiles using regex
        :return: a list of
        """
        reg_people = re.compile(r'">[a-zA-Z0-9._ -]* -|\| LinkedIn')
        self.temp = reg_people.findall(self.all_htmls)
        results = []
        for iteration in (self.temp):
            delete = iteration.replace(' | LinkedIn', '')
            delete = delete.replace(' - LinkedIn', '')
            delete = delete.replace(' profiles ', '')
            delete = delete.replace('LinkedIn', '')
            delete = delete.replace('"', '')
            delete = delete.replace('>', '')
            delete = delete.strip("-")
            if delete != " ":
                results.append(delete)
        return results
    

    
# ls = LinkedinScraper(keyword="Kiran Bodipati",limit=5)
# ls.search()
# links = ls.parse_links()
# profiles = ls.parse_people()

#print(links)

# print(stripped)
# driver = webdriver.Chrome("D:/chromedriver.exe")
# email = "java.oodp.stars@gmail.com"
# password = "javatest"
# actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# # person = Person(links[0], driver=driver)
# print(person.name)
