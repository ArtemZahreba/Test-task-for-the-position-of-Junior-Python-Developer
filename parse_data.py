"""
This code is written for parsing the robota.ua website.
Since the requirement is to avoid class bindings, I used XPATH binding.
This is implemented using a class and a single function.
"""

# Importing Selenium and all necessary modules for page parsing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importing custom error class
from custom_error import CustomError

class ParseData():
    """
    This class is implemented for collecting data from the robota.ua website.

    It has only one function that can be called:

    get_count

    It returns the number of job vacancies on the website.
    """

    def __init__(self):
        self._URL = "https://robota.ua/ru/zapros/junior/ukraine"
        self._XPATH = "/html/body/app-root/div/alliance-jobseeker-vacancies-root-page/div/alliance-jobseeker-desktop-vacancies-page/main/section/div/div"

    def get_count(self, count: int = 0) -> int:
        """
        This function collects the job vacancies count using XPath with Selenium.

        Args:
        - count (int): The number of recursive calls. Used to limit recursion if the site loads slowly or Selenium doesn't find the element.

        Returns:
        - int: The job vacancies count.

        Raises:
        - CustomError: If the element is not found by XPath after the specified number of iterations.
        """

        if count == 10:
            raise CustomError('Element not found by XPATH after 10 attempts')

        driver = webdriver.Chrome()

        driver.get(url=self._URL)

        try:
            # Wait up to 15 seconds for the element to appear on the page
            vacancies_count = WebDriverWait(
                driver,
                15).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        self._XPATH
                    )
                )
            )
            # Here, I edit the found text by first splitting it by newline, then splitting again and joining the first two elements as it is the number we need
            result = "".join(vacancies_count.text.split('\n')[0].split()[:2])

            # Returning the result as an integer
            return int(result)
        except:
            # If an error occurs or the element is not found on the page within 15 seconds
            # Retry the function
            return self.get_count(count=count + 1)
        finally:
            driver.quit()
