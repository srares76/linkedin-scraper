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
sleep(10)

profiles = []
with open(variables.input_file, 'r') as input_file:
    for line in input_file:
        profiles.append(line.strip())

with open(variables.file_name, 'w') as output_file:
    print("[", file=output_file)
    count = 1
    for profile in profiles:
        if profile == "X":
            print(f"Profile {count}/{len(profiles)}: {profile} - SKIPPED\n")
            count += 1
            continue
        close_on_complete = True if profile == profiles[-1] else False
        print(f"Profile {count}/{len(profiles)}: {profile}")
        driver.get(profile)
        sleep(1)
        print("Ready to create Person object")
        person = Person(linkedin_url=profile, driver=driver,
                        get=False, close_on_complete=close_on_complete,
                        idx=count-1)
        person.print(output_file)
        print("Done\n")
        count += 1
        if not close_on_complete:
            print(",", file=output_file)

    print("]", file=output_file)

