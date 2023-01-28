import time
import requests
import json
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException

# ---------------------------------- MY OWN EXCEPTIONS ---------------------------------- #


class LoginException(Exception):
    """ Raised when user delivered wrong login/password """
    pass


# ---------------------------------- VARIABLES/OPTIONS CONIFG  ---------------------------------- #

BASE_URL = ""
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={PC_USER_AGENT}')
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option("detach", True)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()

# ---------------------------------- ADDITIONAL FUNCTIONS  ---------------------------------- #

def login(browser: webdriver.Chrome, email: str, password: str):
    """ Logging into Microsoft Rewards Service """

    # Getting access to the login website
    browser.get('https://login.live.com/')
    is_element_Presence(browser, By.NAME, 'loginfmt', 10)

    # Typing email and clicking next button
    browser.find_element(By.NAME, 'loginfmt').send_keys(email)
    browser.find_element(By.ID, 'idSIButton9').click()

    # Wait for the next logging stage
    time.sleep(3)

    # Typing password and logging in
    is_element_Presence(browser, By.NAME, 'passwd', 10)
    browser.find_element(By.NAME, 'passwd').send_keys(password)

    is_element_Clickable(browser, By.ID, 'idSIButton9', 10)
    browser.find_element(By.ID, 'idSIButton9').click()

    # Wait for the next logging stage
    time.sleep(3)

    # Exception for wrong password.
    is_element_Presence(browser, By.ID, 'idSIButton9', 10)
    is_element_Clickable(browser, By.ID, 'idSIButton9', 10)

    try:
        browser.find_element(By.ID, 'KmsiCheckboxField')
    except NoSuchElementException:
        raise LoginException("Can't find checkbox field - probably user delivered wrong account details.")


    # Trying to click next and finally log in :)
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 3 seconds
        time.sleep(3)
    except NoSuchElementException:
        raise NoSuchElementException("This button doesn't exist. Please open the issue ticket URL: https://github.com/Carmui/Microsoft_Rewards_BOT/issues")

    except ElementNotInteractableException:
        raise ElementNotInteractableException("Interaction problem. Please open the issue ticket URL: https://github.com/Carmui/Microsoft_Rewards_BOT/issues")

    except TimeoutException:
        raise ElementNotInteractableException("Timeout exception. Check all the login details.")

    print(f'{email} status: ', colored('Logged-in !', 'green'))
    # Check Login
    if check_logging() is True:
        result = colored('True', 'green')
    else:
        result = colored('False', 'red')

    print('Check logging function status (True - logged in, False - not logged in): ', result)


def check_logging() -> bool:
    """ Checking if user is currently logged """
    return True


def is_element_Presence(browser: webdriver.Chrome, by: By, selector: str, delay: int):
    """ Function dedicated to wait until element become visible """
    wait = WebDriverWait(browser, delay)
    wait.until(EC.presence_of_element_located((by, selector)))


def is_element_Clickable(browser: webdriver.Chrome, by: By, selector: str, delay: int):
    """ Function dedicated to wait until element become clickable """
    wait = WebDriverWait(browser, delay)
    wait.until(EC.element_to_be_clickable((by, selector)))


def BOT_clickable_elements():
    """ Function dedicated to automate clicking process to earn points from Microsoft Rewards """
    pass


def BOT_writing_elements():
    """ Function dedicated to automate writing process to earn points from Microsoft Rewards """
    pass

# ---------------------------------- MAIN BOT PHASE  ---------------------------------- #

if __name__ == "__main__":
    login(driver, 'test', 'test')
