import pandas as pd
from time import sleep
from Drivers import *
from Scraper import constants as CONST
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LinkedIn():

    def __init__(
        self,
        WebDriver: Chrome | Firefox
    ) -> None:
        
        self.WebDriver = WebDriver
        self.csv_result = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc, traceback):
        return self.WebDriver.__exit__(exc_type, exc, traceback)

    def search(
        self,
        # job,
        # location
    ):
        self.WebDriver.get(url= CONST.JOB_SECTION_URL)
        ActionChains(self.WebDriver).send_keys(Keys.ESCAPE).perform()
        job_input = self.WebDriver.find_element(By.ID , 'job-search-bar-keywords')
        location_input = self.WebDriver.find_element(By.ID , 'job-search-bar-location')
        job_input.clear()
        job_input.send_keys('Data Analyst')
        location_input.clear()
        location_input.send_keys('United States')
        ActionChains(self.WebDriver).send_keys(Keys.ENTER).perform()
        self.scraper()

    def scraper(self):
        jobs_info = list()
        sleep(1)
        jobs = self.WebDriver.find_elements(By.CSS_SELECTOR , 'div.job-search-card')
        for job in jobs[:70]:
            ActionChains(self.WebDriver).scroll_to_element(job).perform()
            job_title = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR , 'div h3')
                )
            ).text
            company = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR , 'div h4 a')
                )
            ).text
            location = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR , 'div div span.job-search-card__location')
                )
            ).text
            list_date = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR , 'div div time')
                )
            ).text
            link = WebDriverWait(driver= job , timeout= 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR , 'a')
                )
            ).get_attribute('href')
            jobs_info.append([job_title,
                              company,
                              location,
                              list_date,
                              link])


        self.csv_result = pd.DataFrame(
            jobs_info,
            columns= ["Job Title" , "Company" , "Location" , "List Date" , "Link"],
        )
        self.csv_result.to_csv('/home/nestark/Codes/.Others/proj_result/test.csv' , index= False)




class search():
    pass

class suggestion():
    pass
