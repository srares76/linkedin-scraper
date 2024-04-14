import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper, Interest, Accomplishment, Contact
import os
from linkedin_scraper import selectors
from time import sleep
import json
import pandas as pd
from .JsonObjects import ExperienceJson, EducationJson, PersonJson
from unidecode import unidecode

class Person(Scraper):
    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        interests=None,
        accomplishments=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
        location=None,
        idx=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.location = location
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self.also_viewed_urls = []
        self.contacts = contacts or []
        self.idx = idx

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def print(self, file):
        jsonExperiences = []
        jsonEducations = []
        for experience in self.experiences:
            jsonExperiences.append(ExperienceJson(experience.institution_name, experience.linkedin_url, experience.from_date,
                                   experience.to_date, experience.description, experience.position_title, experience.duration, experience.location))
        for education in self.educations:
            jsonEducations.append(EducationJson(education.institution_name, education.linkedin_url,
                                  education.from_date, education.to_date, education.description, education.degree))

        sheet = pd.read_excel('./students/excel/studenti-date-personale-2010-2011.xls')
        graduatesInfoRow = sheet.loc[self.idx]

        print(graduatesInfoRow)
        email = unidecode(str(graduatesInfoRow["Email"])) if graduatesInfoRow is not None else ""
        phoneNumber = unidecode(str(graduatesInfoRow["Tel. mobil"])) if graduatesInfoRow is not None else ""
        birthDay = unidecode(str(graduatesInfoRow["Data naşterii"])) if graduatesInfoRow is not None else ""
        highscool = unidecode(str(graduatesInfoRow["Liceu"])) if graduatesInfoRow is not None else ""
        finalPaperName = unidecode(str(graduatesInfoRow["Denumirea lucrării finale"])) if graduatesInfoRow is not None else ""
        highscoolRegion = unidecode(str(graduatesInfoRow["Localitate liceu"])) if graduatesInfoRow is not None else ""
        graduationGrade = unidecode(str(graduatesInfoRow["Medie gen. absolvire"])) if graduatesInfoRow is not None else ""
        universityBachelors = unidecode(str(graduatesInfoRow["Univ Licenţă"])) if graduatesInfoRow is not None else ""
        facultyBachelors = unidecode(str(graduatesInfoRow["Facultate Licenţă"])) if graduatesInfoRow is not None else ""
        bacYear = unidecode(str(graduatesInfoRow["An BAC"])) if graduatesInfoRow is not None else ""
        bachelorsFromYear = unidecode(str(graduatesInfoRow["An admitere licenta"])) if graduatesInfoRow is not None else ""


        jsonPerson = PersonJson(self.name, self.location, self.company, self.linkedin_url,
                                self.job_title, self.about,  jsonExperiences, jsonEducations,
                                email, birthDay, phoneNumber, highscool, highscoolRegion,
                                finalPaperName, graduationGrade, universityBachelors, facultyBachelors,
                                bacYear, bachelorsFromYear)

        print(jsonPerson.toJSON(), file=file)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience: Experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        self.scrape_logged_in(close_on_complete=close_on_complete)

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME, "pv-top-card-profile-picture").find_element(By.TAG_NAME, "img").get_attribute("title")
        except:
            return False

    def get_experiences(self):
        url = os.path.join(self.linkedin_url, "details/experience")
        self.driver.get(url)
        sleep(2)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        for position in main_list.find_elements(By.XPATH, "li"):
            position = position.find_element(
                By.CSS_SELECTOR, '[data-view-name="profile-component-entity"]')
            company_logo_elem, position_details = position.find_elements(
                By.XPATH, "*")

            # company elem
            company_linkedin_url = company_logo_elem.find_element(
                By.XPATH, "*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(
                By.XPATH, "*")
            position_summary_details = position_details_list[0] if len(
                position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(
                position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(
                By.XPATH, "*").find_elements(By.XPATH, "*")

            work_times = ""
            position_title = ""
            location = ""
            company = ""
            if len(outer_positions) == 4:
                position_title = outer_positions[0].find_element(
                    By.TAG_NAME, "span").text
                company = outer_positions[1].find_element(
                    By.TAG_NAME, "span").text
                work_times = outer_positions[2].find_element(
                    By.TAG_NAME, "span").text
                location = outer_positions[3].find_element(
                    By.TAG_NAME, "span").text
            elif len(outer_positions) == 3:
                if "·" in outer_positions[2].text:
                    position_title = outer_positions[0].find_element(
                        By.TAG_NAME, "span").text
                    company = outer_positions[1].find_element(
                        By.TAG_NAME, "span").text
                    work_times = outer_positions[2].find_element(
                        By.TAG_NAME, "span").text
                    location = ""
                else:
                    position_title = ""
                    company = outer_positions[0].find_element(
                        By.TAG_NAME, "span").text
                    work_times = outer_positions[1].find_element(
                        By.TAG_NAME, "span").text
                    location = outer_positions[2].find_element(
                        By.TAG_NAME, "span").text

            times = work_times.split("·")[0].strip() if work_times else ""
            duration = work_times.split("·")[1].strip() if len(
                work_times.split("·")) > 1 else None

            from_date = " ".join(times.split(" ")[:2]) if times else ""
            to_date = " ".join(times.split(" ")[3:]) if times else ""

            description = position_summary_text.text if position_summary_text else ""

            experience = Experience(
                position_title=position_title,
                from_date=from_date,
                to_date=to_date,
                duration=duration,
                location=location,
                description=description,
                institution_name=company,
                linkedin_url=company_linkedin_url
            )
            self.add_experience(experience)

    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        sleep(2)
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if (main_list is None):
            return
        for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
            position = position.find_element(
                By.CSS_SELECTOR, '[data-view-name="profile-component-entity"]'
            )
            institution_logo_elem, position_details = position.find_elements(
                By.XPATH, "*")

            # company elem
            institution_linkedin_url = institution_logo_elem.find_element(
                By.XPATH, "*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(
                By.XPATH, "*")
            position_summary_details = position_details_list[0] if len(
                position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(
                position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(
                By.XPATH, "*").find_elements(By.XPATH, "*")

            institution_name = outer_positions[0].find_element(
                By.TAG_NAME, "span").text
            degree = outer_positions[1].find_element(By.TAG_NAME, "span").text

            if len(outer_positions) > 2:
                times = outer_positions[2].find_element(
                    By.TAG_NAME, "span").text

                split_times = times.split(" ")
                if len(split_times) == 1:
                    from_date = split_times[0]
                    to_date = split_times[0]
                elif len(split_times) == 5:
                    from_date = " ".join(times.split(" ")[:2])
                    to_date = " ".join(times.split(" ")[3:])
                else:
                    from_date = split_times[0]
                    to_date = split_times[2]
            else:
                from_date = None
                to_date = None

            description = position_summary_text.text if position_summary_text else ""

            education = Education(
                from_date=from_date,
                to_date=to_date,
                description=description,
                degree=degree,
                institution_name=institution_name,
                linkedin_url=institution_linkedin_url
            )
            self.add_education(education)

    def get_name_and_location(self):
        name = self.driver.find_element(
            By.CLASS_NAME, "text-heading-xlarge").text
        location = self.driver.find_element(
            By.XPATH, "//*[@id=\"profile-content\"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]").text
        self.name = name
        self.location = unidecode(location)

    def get_about(self):
        try:
            about = self.driver.find_element(By.ID, "about").find_element(
                By.XPATH, "..").find_element(By.CLASS_NAME, "display-flex").text
        except NoSuchElementException:
            about = None
        self.about = about

    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        print("Beginning to parse")

        self.focus()
        self.wait(5)

        # open to work
        self.open_to_work = self.is_open_to_work()

        # get about
        self.get_about()
        print("Got about")

        # get name and location
        if self.name is None:
            self.get_name_and_location()
        print("Got name and location")

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        # get experience
        self.get_experiences()
        print("Got experiences")

        # get education
        self.get_educations()
        print("Got educations")

        if close_on_complete:
            print("Closing the driver")
            driver.quit()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return "<Person {name}\n\nAbout\n{about}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nInterest\n{int}\n\nAccomplishments\n{acc}\n\nContacts\n{conn}>".format(
            name=self.name,
            about=self.about,
            exp=self.experiences,
            edu=self.educations,
            int=self.interests,
            acc=self.accomplishments,
            conn=self.contacts,
        )
