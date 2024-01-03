import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper 
import os
from time import sleep
from typing import List


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
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=False,
        time_to_wait_after_login=0,
        location=None,
    ):
        self.linkedin_url:str = linkedin_url
        self.name:str = name
        self.location: str = location
        self.about: str = about or []
        self.experiences: List[Experience] = experiences or []
        self.educations: List[Education] = educations or []
        # # # self.interests = interests or []
        # # # self.accomplishments = accomplishments or []
        # # self.also_viewed_urls = []
        # self.contacts = contacts or []

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

    def print(self):
        print(f"LinkedIn URL: {self.linkedin_url}\n")
        print(f"Name: {self.name}\n")
        print(f"Job Title: {self.job_title}'\n")
        print(f"Company: {self.company}\n")
        print(f"About: {self.about}\n")
        print(f"Location: {self.location}\n")
        for experience in self.experiences:
            print(f"Experience: {experience}\n")
        for education in self.educations:
            print(f"Education: {education}\n")
        print(f"Is open to work: {self.open_to_work}\n")

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
        # if self.is_signed_in():
        self.scrape_logged_in(close_on_complete=close_on_complete)
        # else:
        #     print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
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
        for position in main_list.find_elements(By.XPATH,"li"):
            position = position.find_element(By.CLASS_NAME,"pvs-entity--padded")
            company_logo_elem, position_details = position.find_elements(By.XPATH,"*")

            # company elem
            company_linkedin_url = company_logo_elem.find_element(By.XPATH,"*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(By.XPATH,"*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

            if len(outer_positions) == 4:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                location = outer_positions[3].find_element(By.TAG_NAME,"span").text
            elif len(outer_positions) == 3:
                if "·" in outer_positions[2].text:
                    position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                    location = ""
                else:
                    position_title = ""
                    company = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    location = outer_positions[2].find_element(By.TAG_NAME,"span").text

            print(work_times)
            times = work_times.split("·")[0].strip() if work_times else ""
            duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None

            # from_date = " ".join(times.split(" ")[:2]) if times else ""
            # to_date = " ".join(times.split(" ")[3:]) if times else ""
            split_times = times.split("-")
            if (len(split_times) == 2):
                from_date = split_times[0]
                to_date = split_times[1]
            else:
                from_date = None
                to_date = times

            # if position_summary_text and len(position_summary_text.find_element(By.CLASS_NAME,"pvs-list").find_element(By.CLASS_NAME,"pvs-list").find_elements(By.XPATH,"li")) > 1:
            #     descriptions = position_summary_text.find_element(By.CLASS_NAME,"pvs-list").find_element(By.CLASS_NAME,"pvs-list").find_elements(By.XPATH,"li")
            #     for description in descriptions:
            #         res = description.find_element(By.TAG_NAME,"a").find_elements(By.XPATH,"*")
            #         position_title_elem = res[0] if len(res) > 0 else None
            #         work_times_elem = res[1] if len(res) > 1 else None
            #         location_elem = res[2] if len(res) > 2 else None


            #         location = location_elem.find_element(By.XPATH,"*").text if location_elem else None
            #         position_title = position_title_elem.find_element(By.XPATH,"*").find_element(By.TAG_NAME,"*").text if position_title_elem else ""
            #         work_times = work_times_elem.find_element(By.XPATH,"*").text if work_times_elem else ""
            #         times = work_times.split("·")[0].strip() if work_times else ""
            #         duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None
            #         from_date = " ".join(times.split(" ")[:2]) if times else ""
            #         to_date = " ".join(times.split(" ")[3:]) if times else ""

            #         experience = Experience(
            #             position_title=position_title,
            #             from_date=from_date,
            #             to_date=to_date,
            #             duration=duration,
            #             location=location,
            #             description=description,
            #             institution_name=company,
            #             linkedin_url=company_linkedin_url
            #         )
            #         self.add_experience(experience)
            # else:
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
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity--padded"):
            institution_logo_elem, position_details = position.find_elements(By.XPATH,"*")

            # company elem
            institution_linkedin_url = institution_logo_elem.find_element(By.XPATH,"*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(By.XPATH,"*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

            institution_name = outer_positions[0].find_element(By.TAG_NAME,"span").text
            degree = outer_positions[1].find_element(By.TAG_NAME,"span").text

            if len(outer_positions) > 2:
                times = outer_positions[2].find_element(By.TAG_NAME,"span").text

                split_times = times.split("-")
                if (len(split_times) == 2):
                    from_date = split_times[0]
                    to_date = split_times[1]
                else:
                    from_date = None
                    to_date = times

                # split_times = times.split(" ")
                # if len(split_times) == 2:
                #     from_date = ""
                #     to_date = times
                # elif len(split_times) == 5:
                #     from_date = " ".join(times.split(" ")[:2])
                #     to_date = " ".join(times.split(" ")[3:])
                # else:
                #     from_date = split_times[0]
                #     to_date = split_times[2]
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
        top_panels = self.driver.find_elements(By.CLASS_NAME,"pv-text-details__left-panel")
        if len(top_panels) != 2:
            return
        self.name = top_panels[0].find_elements(By.XPATH,"*")[0].text
        self.location = top_panels[1].find_element(By.TAG_NAME,"span").text


    def get_about(self):
        try:
            about = self.driver.find_element(By.ID,"about").find_element(By.XPATH,"..").find_element(By.CLASS_NAME,"display-flex").text
        except NoSuchElementException :
            about=None
        self.about = about

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        # duration = None

        # root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.CLASS_NAME,
        #             self.__TOP_CARD,
        #         )
        #     )
        # )
        self.focus()
        self.wait(5)

        # get name and location
        if self.name is None:
            self.get_name_and_location()

        # open to work
        self.open_to_work = self.is_open_to_work()

        # get about
        self.get_about()

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get experience
        self.get_experiences()

        # get education
        self.get_educations()

        driver.get(self.linkedin_url)

        # # get connections
        # try:
        #     driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        #     _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
        #     )
        #     connections = driver.find_element(By.CLASS_NAME, "mn-connections")
        #     if connections is not None:
        #         for conn in connections.find_elements(By.CLASS_NAME, "mn-connection-card"):
        #             anchor = conn.find_element(By.CLASS_NAME, "mn-connection-card__link")
        #             url = anchor.get_attribute("href")
        #             name = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__name").text.strip()
        #             occupation = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__occupation").text.strip()

        #             contact = Contact(name=name, occupation=occupation, url=url)
        #             self.add_contact(contact)
        # except:
        #     connections = None

        if close_on_complete:
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