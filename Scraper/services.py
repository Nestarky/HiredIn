from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from time import sleep
from typing import Literal

from Drivers import *
from Scraper import constants as CONST


class LinkedIn():

    def __init__(
        self,
        WebDriver: Literal['Chrome', 'Firefox']
    ) -> None:
        
        self.WebDriver = Chrome() if WebDriver == 'Chrome' else Firefox()

    def search(
        self,
        job,
        location
    ):
        with Search(
            LinkedIn_session= self,
            Job= job,
            Location= location
        ) as Search_session:
            result = Search_session.fetch()

        return result




class Search():

    def __init__(
        self,
        LinkedIn_session: LinkedIn,
        Job: str,
        Location: str
        
    ) -> None:
        
        self.LinkedIn_session = LinkedIn_session
        self.Result = None

        self.Job = Job.replace(' ' , '%20')
        self.Location = Location.replace(' ' , '%20')

        self.LinkedIn_session.WebDriver.get(
            CONST.JOB_SEARCH_URL.format(
                self.Job, 
                self.Location
            )
        )
        
        ActionChains(
            driver= self.LinkedIn_session.WebDriver
        ).send_keys(Keys.ESCAPE).perform()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, traceback):
        #TODO Handle cookies
        pass

    def fetch(self):

        jobs_info = list()
        jobs = WebDriverWait(self.LinkedIn_session.WebDriver, timeout= 5).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    CONST.JOB_CARD_ADDRESS
                )
            )
        )

        for job in jobs[:50]:
            
            title = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR, 
                        CONST.TITLE_ADDRESS
                    )
                )
            ).text
            company = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        CONST.COMPANY_ADDRESS
                    )
                )
            ).text
            location = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        CONST.LOCATION_ADDRESS
                    )
                )
            ).text
            list_date = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        CONST.LIST_DATE_ADDRESS
                    )
                )
            ).text
            link = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        CONST.LINK_ADDRESS
                    )
                )
            ).get_attribute('href')
            
            jobs_info.append([title,
                              company,
                              location,
                              list_date,
                              link])
        
        self.Result = pd.DataFrame(
            jobs_info,
            columns= ["Job Title" , "Company" , "Location" , "List Date" , "Link"]
        )

        return self.Result