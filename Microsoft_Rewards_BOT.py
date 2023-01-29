import time
import os
import json
from colorama import Fore, Back, Style
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


# ---------------------------------- VARIABLES/CHROME OPTIONS CONIFG  ---------------------------------- #

BASE_URL = ""
BASE_EMAIL = "EXAMPLE_EMAIL"
BASE_PASSWORD = "EXAMPLE_PASSWORD"
ACCOUNTS = []
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'

options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={PC_USER_AGENT}')
options.add_argument('disable-blink-features=AutomationControlled')
options.add_experimental_option("detach", True)


def driver_manager(opt: webdriver.ChromeOptions() = options) -> webdriver.Chrome:
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=opt)
    driver.maximize_window()
    return driver


# ---------------------------------- ADDITIONAL FUNCTIONS  ---------------------------------- #

def login(browser: webdriver.Chrome, email: str, password: str):
    """ Logging into Microsoft Rewards Service """

    print(Fore.CYAN + f""" 
Login procedure for incoming account details:
email: {email}
password: {password}
          """)

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
        raise NoSuchElementException("This button doesn't exist. Please open the issue ticket.    |    URL: https://github.com/Carmui/Microsoft_Rewards_BOT/issues")

    except ElementNotInteractableException:
        raise ElementNotInteractableException("Interaction problem. Please open the issue ticket.    |    URL: https://github.com/Carmui/Microsoft_Rewards_BOT/issues")

    except TimeoutException:
        raise ElementNotInteractableException("Timeout exception. Check all the login details.")

    print(Fore.WHITE + f'{email} status: ', Fore.GREEN + 'Logged-in!')

    # Additional login check
    if check_logging(browser) is True:
        color = Fore.GREEN
        result = 'Logged-in!'
    else:
        color = Fore.RED
        result = 'Not logged-in!'

    print(Fore.WHITE + 'Additional check status:', color + result)


def check_logging(browser: webdriver.Chrome, ) -> bool:
    """ Checking if user is currently logged """
    # We are going to check logs in 2 different ways (2 different websites)
    current_url = browser.current_url
    time.sleep(2)

    # Cookies accept - else way pass
    try:
        browser.find_element(By.XPATH, '//*[@id="cookie-banner"]/div/div[2]/button[1]').click()
    except:
        pass


    if current_url.split('?')[0] == 'https://account.microsoft.com/':
        print('xd')
        return True
    elif current_url == 'https://bing.com/':
        print('xp')
        return True
    else:
        print('wat')
        return True




def is_element_Presence(browser: webdriver.Chrome, by: By, selector: str, delay: int):
    """ Function dedicated to wait until element become presence """
    wait = WebDriverWait(browser, delay)
    wait.until(EC.presence_of_element_located((by, selector)))


def is_element_Clickable(browser: webdriver.Chrome, by: By, selector: str, delay: int):
    """ Function dedicated to wait until element become clickable """
    wait = WebDriverWait(browser, delay)
    wait.until(EC.element_to_be_clickable((by, selector)))


def get_accounts(file_path: str) -> dict:
    """
        Get accounts from json file or create one if file doesn't exist.
        Little advice: do not create more than 4 accounts (IP may be tracked and you will probably get banned)
    """
    try:
        accounts = json.load(open(file_path, "r"))
    except FileNotFoundError:
        with open(file_path, 'w') as f:

            f.write(json.dumps([
            {
                "email": BASE_EMAIL,
                "password": BASE_PASSWORD
            },
            {
                "email": BASE_EMAIL,
                "password": BASE_PASSWORD
            }
            ], indent=5))


        print("""
[BOT] New file was created. Please update account details to proceed.
[BOT] If you want to add more accounts -> follow the structure created in the file. New accounts need to be separeted with a comma.
             """)
        accounts = json.load(open(file_path, "r"))

    return accounts

def BOT_clickable_elements():
    """ Function dedicated to automate clicking process to earn points from Microsoft Rewards """
    pass


def BOT_writing_elements():
    """ Function dedicated to automate writing process to earn points from Microsoft Rewards """
    pass


def close_phase(browser: webdriver.Chrome):
    """ Function dedicated to close the BOT process. """
    print(Fore.MAGENTA + """
Work done. Quitting automation procedure.   
--------------------------------------------------------------------------------------------------------------------------------
    """)
    browser.quit()


# ---------------------------------- MAIN BOT PHASE  ---------------------------------- #

if __name__ == "__main__":
    print(Fore.CYAN + """
                                ╔═╗╔═╗                      ╔═╗ ╔╗     ╔═══╗╔═══╗╔╗╔╗╔╗╔═══╗╔═══╗╔═══╗╔═══╗    ╔══╗ ╔═══╗╔════╗
                                ║║╚╝║║                      ║╔╝╔╝╚╗    ║╔═╗║║╔══╝║║║║║║║╔═╗║║╔═╗║╚╗╔╗║║╔═╗║    ║╔╗║ ║╔═╗║║╔╗╔╗║
                                ║╔╗╔╗║╔╗╔══╗╔═╗╔══╗╔══╗╔══╗╔╝╚╗╚╗╔╝    ║╚═╝║║╚══╗║║║║║║║║ ║║║╚═╝║ ║║║║║╚══╗    ║╚╝╚╗║║ ║║╚╝║║╚╝
                                ║║║║║║╠╣║╔═╝║╔╝║╔╗║║══╣║╔╗║╚╗╔╝ ║║     ║╔╗╔╝║╔══╝║╚╝╚╝║║╚═╝║║╔╗╔╝ ║║║║╚══╗║    ║╔═╗║║║ ║║  ║║  
                                ║║║║║║║║║╚═╗║║ ║╚╝║╠══║║╚╝║ ║║  ║╚╗    ║║║╚╗║╚══╗╚╗╔╗╔╝║╔═╗║║║║╚╗╔╝╚╝║║╚═╝║    ║╚═╝║║╚═╝║ ╔╝╚╗ 
                                ╚╝╚╝╚╝╚╝╚══╝╚╝ ╚══╝╚══╝╚══╝ ╚╝  ╚═╝    ╚╝╚═╝╚═══╝ ╚╝╚╝ ╚╝ ╚╝╚╝╚═╝╚═══╝╚═══╝    ╚═══╝╚═══╝ ╚══╝ 
                                                                 by Mateusz Michalowski (@carmui)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    """)

    # Getting accounts json path
    accounts_path = os.path.dirname(os.path.abspath(__file__)) + '/accounts.json'
    ACCOUNTS = get_accounts(accounts_path)

    for account in ACCOUNTS:
        # Getting browse driver
        chrome_browser = driver_manager()

        # Login to the server with the first account
        login(chrome_browser, account["email"], account["password"])

        time.sleep(15)
        close_phase(chrome_browser)
