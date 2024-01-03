from parsel import Selector
from scraper.person import Person
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Scraper():
    def __init__(self, driver):
        self.driver = driver
    
    def scrape_profile(self, profile_url: str, search_prompt: str):
        self.driver.get(profile_url)
        sleep(1)
        sel = Selector(text=self.driver.page_source)
        name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge")]/text()').extract_first()
        if name:
            name = name.strip()
        else:
            name = 'No Result'
        location = sel.xpath('//*[starts-with(@class, "text-body-small")]/text()').extract_first()
        if location:
            location = location.strip()
        else:
            location = 'No Result'
        person = Person(linkedin_url=profile_url,
                    driver=self.driver, name=name, location=location, get=False)
        return person

