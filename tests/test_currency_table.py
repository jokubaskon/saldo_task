import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

    @classmethod
    def setUpClass(cls):
        cls.browser_name = 'firefox'
        cls.driver = get_browser(cls.browser_name)
        cls.driver.maximize_window()
        

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.base_url = "https://www.xe.com/currencytables/"
        self.date = "2023-02-01"

    # ----------------------------------------------- TESTS --------------------------------------------------------

    def test_currency_and_date_widget_exists(self):
        self.driver.get(self.base_url)
        table = self.driver.find_element(By.XPATH ,"/html/body/div[1]/div[4]/div[2]/section/form")
        self.assertIsNotNone(table, "Currency table should exist on the page")

    # Parameterize tests
    #
    # Currency code to search for | Expected Value | Label | Date | Search regex
    @parameterized.expand([
        
        ("USD", "1.0918121631244302", "usd_per_eur", dates[0], eur_regex),
        ("GBP", "0.8871386636267415", "gbp_per_eur", dates[0], eur_regex),
        ("PLN", "3.9897698476779544", "pln_per_usd", dates[1], usd_regex),
        # Add more test cases as needed
    ])
    def test_currency_value(self, currency_code, expected_value, label, date, regex):
        currency_data = self.extract_data(currency_code, date)
        match = re.search(regex, currency_data)
        self.assertIsNotNone(match, f"{currency_code} data not found.")
        actual_value = match.group(2)

        self.assertEqual(actual_value, expected_value, f"Expected value '{expected_value}', but got '{actual_value}'.")


    # ----------------------------------------------- Helper methods ----------------------------------------------
    def extract_data(self, currency, date):
        self.driver.get(self.base_url)
        sleep(1)

        try:
            currency_dropdown_main = self.driver.find_element(By.XPATH, '//*[@id="currency"]')
            currency_dropdown_main.click()
            currency_dropdown_child = self.driver.find_element(By.CSS_SELECTOR, 'input.sc-73a056d4-0:nth-child(1)')
            sleep(1)
            currency_dropdown_child.send_keys(currency)
            sleep(1)
            currency_dropdown_child.send_keys(Keys.RETURN)
        except:
            self.fail("Currency dropdown failed")

        try:
            date_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/section/form/div[2]/div/div[1]/input")
            date_input.clear()
            date_input.click()
            date_input.send_keys(date)
            date_input.send_keys(Keys.RETURN)
            sleep(1)
        except NoSuchElementException:
            self.fail("Date input does not exist on the page")

        try:
            currencyData = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[3]/section/div[2]/div/table")
            return self.get_table_data_as_string(currencyData)
        except NoSuchElementException:
            self.fail("Table does not exist")

    def get_table_data_as_string(self, table):
        table_data = ""
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                table_data += cell.text + "\t"
            table_data += "\n"  # Newline after each row
        return table_data


if __name__ == "__main__":
    unittest.main()