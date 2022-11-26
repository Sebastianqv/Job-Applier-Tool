from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import *
from urllib.parse import quote
import time

class ApplierInstance():
    """Class for creating Applier instances."""

    def __init__(self, username:str, password:str, fieldName:str, onlyEasyApply:bool = True):
        """Constructor for the ApplierInstance class."""
        service = Service(executable_path="./webDrivers/chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.jobList = {}
        self.ranThrough = False
        self.username = username
        self.password = password
        self.fieldName = fieldName
        self.onlyEasyApply = onlyEasyApply

    def start(self):
        """Starts the webDriver for job search."""
        try:
            #Log in
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            usernameInput = self.driver.find_element(By.CSS_SELECTOR, "input#username")
            usernameInput.send_keys(self.username)
            passwordInput = self.driver.find_element(By.CSS_SELECTOR, "input#password")
            passwordInput.send_keys(self.password, Keys.ENTER)
            time.sleep(2)

            searchUrl = "https://www.linkedin.com/jobs/search/?"
            if self.onlyEasyApply:
                searchUrl += "f_AL=true&"
            searchUrl += "keywords=" + quote(self.fieldName)

            self.driver.get(searchUrl)
            time.sleep(3)

            jobListContainer = self.driver.find_element(By.CSS_SELECTOR, "ul.scaffold-layout__list-container")
            scroll_origin = ScrollOrigin.from_element(jobListContainer)
            ActionChains(self.driver).scroll_from_origin(scroll_origin, 0, 3000).perform()
            time.sleep(1)

            easyApplyJobs = jobListContainer.find_elements(By.CSS_SELECTOR, "li-icon.mr1")
            for job in easyApplyJobs:
                title = job.find_element(By.XPATH, "./..")\
                .find_element(By.XPATH, "./..")\
                .find_element(By.XPATH, "./..")\
                .find_element(By.CSS_SELECTOR, "a.job-card-list__title")

                self.jobList[title.text] = title.get_attribute("href")

            self._toggleRanThrough()

        except AttributeError:
            print("Could not find any jobs")

    def _toggleRanThrough(self):
        """
        Toggles whether the job search has concluded.
        Default is False.
        """
        self.ranThrough = not self.ranThrough

    def getJobList(self):
        """
        Get the list of jobs.

        Returns:
            jobList (dict): A Dictionary in title/url (key/value) pairs.
        """
        return self.jobList

    def apply(self, url:str):
        """
        Begin the process of applying to a job.

        Parameters:
            url (string): Url to the job to apply to/
        """
        try:
            self.driver.get(url)
            time.sleep(3)
        except InvalidArgumentException:
            print("Could not find url")

    def exit(self):
        """Closes the webDriver instance."""
        self.driver.quit()