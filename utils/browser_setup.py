from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver

# Browsers available for testing
def get_browser(browser_name):
    if browser_name.lower() == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser_name.lower() == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        # Uncomment to use local geckodriver
        #options = Options()
        #options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        #driver = webdriver.Firefox(options)
    return driver