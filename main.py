import variables
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from scrape_profile import Scraper
from utils import studied_at_politehnica


driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')

username = driver.find_element(By.ID, 'session_key')
username.send_keys(variables.my_username) # username field

password = driver.find_element(By.NAME, 'session_password')
password.send_keys(variables.my_password) # password field

log_in_button = driver.find_element(By.CSS_SELECTOR,'[type="submit"]')
log_in_button.click()
sleep(10) # for manual CAPTCHA solving when needed

# profile = 'https://www.linkedin.com/in/andrei-gabriel-popescu/'
# profile = 'https://www.linkedin.com/in/rares-constantin-stefan-7b04b3209/'
# profile = 'https://www.linkedin.com/in/irina-grigore7/'
# profile = 'https://www.linkedin.com/in/irina-grigore-9389723a/'

# profile_scraper = Scraper(driver=driver)
# person_data = profile_scraper.scrape_profile(profile)
# person_data.print()

search_prompt = "Georgian Cucu"
# search_prompt = "Rares Stefan"
people_list_URL = 'https://www.linkedin.com/search/results/people/?keywords=' + search_prompt.replace(" ", "%20")

driver.get(people_list_URL)

# Extract all profile URLs from the search results
profiles = driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://www.linkedin.com/in/")]')
profile_urls = []
for profile in profiles:
    if (profile.get_dom_attribute('href') not in profile_urls):
        profile_urls.append(profile.get_dom_attribute('href').split('?')[0])

profile_scraper = Scraper(driver=driver)
can_stop = False

# remove duplicates from profile_urls
profile_urls = list(dict.fromkeys(profile_urls))

for profile_url in profile_urls:
    print(profile_url)

for profile_url in profile_urls:
    # if 'rares-constantin-stefan-7b04b3209' not in str(profile_url):
    #     continue
    person_data = profile_scraper.scrape_profile(profile_url)
    print("done with a person")

    was_student = studied_at_politehnica(person_data.educations)
    if (was_student):
        person_data.print()
        break;
