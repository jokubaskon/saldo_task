import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_setup import get_browser
from time import sleep
import re
from parameterized import parameterized

class TestCurrencyTable(unittest.TestCase):
    dates = [
    "2023-02-01",
    "2024-01-03",
    # Add more dates as needed
    ]
    eur_regex = r"Euro\s+(\d+\.\d+)\s+(\d+\.\d+)"
    usd_regex = r"US Dollar\s+(\d+\.\d+)\s+(\d+\.\d+)"
    base_url = "https://www.xe.com/currencytables/"
       

    # ----------------------------------------------- TESTS --------------------------------------------------------

    # Parameterize tests
    #
    # Label | Expected Value | Currency value to search for | Date | browser | Search regex
    @parameterized.expand([
        
        ("usd_per_eur_ff", "1.0918121631244302", "USD", dates[0], "firefox", eur_regex),
        ("gbp_per_eur_ff", "0.8871386636267415", "GBP", dates[0], "firefox", eur_regex),
        ("pln_per_usd_ff", "3.9897698476779544", "PLN", dates[1], "firefox", usd_regex),
        ("usd_per_eur_chrome", "1.0918121631244302", "USD", dates[0], "chrome", eur_regex),
        ("gbp_per_eur_chrome", "0.8871386636267415", "GBP", dates[0], "chrome", eur_regex),
        ("pln_per_usd_chrome", "3.9897698476779544", "PLN", dates[1], "chrome", usd_regex),
        # Add more test cases as needed
    ])
    def test_currency_value(self, label, expected_value, currency_code, date, browser, regex):
        print(f"Testing currency value {label}")
        self.setup_driver(browser)
        currency_data = self.extract_data(currency_code, date, browser)
        match = re.search(regex, currency_data)
        self.assertIsNotNone(match, f"{currency_code} data not found.")
        actual_value = match.group(2)
        self.driver.quit()

        self.assertEqual(actual_value, expected_value, f"Expected value '{expected_value}', but got '{actual_value}'.")


    # ----------------------------------------------- Helper methods ----------------------------------------------
    def setup_driver(self, browser_name):
        self.browser_name = browser_name
        self.driver = get_browser(browser_name)
        self.driver.maximize_window()

    
    # Enters required data and returns currency values as a string
    def extract_data(self, currency, date, browser):
        self.driver.get(self.base_url)
        sleep(1)

        # Enter currency code
        try:
            currency_dropdown_main = self.driver.find_element(By.XPATH, '//*[@id="currency"]')
            currency_dropdown_main.click()
            currency_dropdown_child = self.driver.find_element(By.CSS_SELECTOR, 'input.sc-73a056d4-0:nth-child(1)')
            currency_dropdown_child.send_keys(currency)
            sleep(1)  # required for the currencies to load
            currency_dropdown_child.send_keys(Keys.RETURN)
        except:
            self.fail("Failed to enter currency code.")

        # Enter date
        try:
            date_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/section/form/div[2]/div/div[1]/input")
            if(browser == "firefox"):
                date_input.clear()
            # clear() doesn't work on chrome on this input
            elif(browser == "chrome"):
                date_input.send_keys(Keys.CONTROL + "a")
                date_input.send_keys(Keys.DELETE)
            date_input.click()
            date_input.send_keys(date)
            date_input.send_keys(Keys.RETURN)
            sleep(1)
        except:
            self.fail("Failed to enter date.")

        # Retrieve data from the currency table
        try:
            currencyData = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[3]/section/div[2]/div/table")
            return self.get_table_data_as_string(currencyData)
        except:
            self.fail("Failed to retrieve currency data.")

    # Returns currency string
    def get_table_data_as_string(self, table):
        table_data = ""
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                table_data += cell.text + "\t"
            table_data += "\n"
        return table_data


if __name__ == "__main__":
    unittest.main()