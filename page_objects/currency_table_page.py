from selenium.webdriver.common.by import By

class CurrencyTablePage:
    # Locators
    CURRENCY_INPUT_INITIAL = (By.ID, "currency")
    CURRENCY_INPUT_AFTERCLICK = (By.CSS_SELECTOR, 'input.sc-73a056d4-0:nth-child(1)') # no ID
    DATE_INPUT = (By.CSS_SELECTOR, "input.sc-73a056d4-0:nth-child(2)") # no ID
    CURRENCY_TABLE = (By.ID, "table-section")