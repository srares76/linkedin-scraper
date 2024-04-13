import variables
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from scraper.person import Person

driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')

username = driver.find_element(By.ID, 'session_key')
username.send_keys(variables.my_username)  # username field

password = driver.find_element(By.NAME, 'session_password')
password.send_keys(variables.my_password)  # password field

log_in_button = driver.find_element(
    By.CSS_SELECTOR, '[type="submit"]')  # submit button
log_in_button.click()  # click the submit button
# sleep(10)

# profiles = ['https://www.linkedin.com/in/rares-constantin-stefan',
#             'https://www.linkedin.com/in/marius-avramescu-a4540337']
profiles = ['https://www.linkedin.com/in/rares-constantin-stefan',
            'https://www.linkedin.com/in/rares-constantin-stefan']
# profiles = []
# with open('students/2010.txt', 'r') as input_file:
#     for line in input_file:
#         profiles.append(line.strip())

with open(variables.file_name, 'w') as output_file:
    for profile in profiles:
        print("beginning", profile)
        driver.get(profile)
        print("parsing")
        sleep(1)
        print("Ready to create Person object")
        person = Person(linkedin_url=profile, driver=driver, get=False)
        person.print(output_file)
        print("parsed")
