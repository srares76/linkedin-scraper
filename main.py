import variables
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from parsel import Selector

from scraper.person import Person


driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')
# sleep(1)

username = driver.find_element(By.ID, 'session_key')
username.send_keys(variables.my_username) # username field

password = driver.find_element(By.NAME, 'session_password')
password.send_keys(variables.my_password) # password field

log_in_button = driver.find_element(By.CSS_SELECTOR,'[type="submit"]') # submit button
log_in_button.click() # click the submit button
# sleep(10)

profile = 'https://www.linkedin.com/in/andrei-gabriel-popescu/'
# profile = 'https://www.linkedin.com/in/rares-constantin-stefan-7b04b3209/'
sel = Selector(text=driver.page_source)

fields = ['Name','Job Title','Company','University','Location','URL']

with open(variables.file_name, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fields)

    driver.get(profile)
    sel = Selector(text=driver.page_source)
    sleep(1)
    name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge")]/text()').extract_first()
    if name:
        name = name.strip()
    else:
        name = 'No Result'
    job_title = sel.xpath('//*[starts-with(@class, "inline-show-more-text")]/text()').extract_first()
    if job_title:
        job_title = job_title.strip()
    else:
        job_title = 'No Result'
    company = sel.xpath('//*[starts-with(@aria-label, "Current company")]/text()').extract_first()
    if company:
        company = company.strip()
    else:
        company = 'No Result'
    university = sel.xpath('//*[starts-with(@aria-label, "Education")]/text()').extract_first()
    if university:
        university = university.strip()
    else:
        university = 'No Result'
    location = sel.xpath('//*[starts-with(@class, "text-body-small")]/text()').extract_first()
    if location:
        location = location.strip()
    else:
        location = 'No Result'
    linkedin_url = driver.current_url
    writer.writerow([name, job_title, company, university, location, linkedin_url])
    person = Person(linkedin_url=profile,
                  driver=driver, name=name, location=location, get=False)
    person.print()


