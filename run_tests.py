import unittest
import xmlrunner
import os
import argparse
from datetime import datetime
from utils.browser_setup import SUPPORTED_BROWSERS

def parse_args():
    parser = argparse.ArgumentParser(description="Run Selenium tests with a specified browser. If browser is not specified, runs with all of them.")
    parser.add_argument("--browser", type=str, help="Browser to use for tests (chrome, firefox) if flag is not specified, runs tests on both of the browsers.")
    args = parser.parse_args()
    return args

def set_environment(args):
    if args.browser:
        # Set the browser flag as an environment variable
        check_browser(args.browser)
        os.environ["BROWSER_FLAG"] = args.browser
    else:
        # Run tests for both browsers by default
        os.environ["BROWSER_FLAG"] = "both"

def check_browser(browser):
    browser = browser.lower()
    if browser not in SUPPORTED_BROWSERS:
        raise ValueError(f"{browser} is not supported.") 

if __name__ == "__main__":
    args = parse_args()
    set_environment(args)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests")

    output_dir = "test-reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    output_file = os.path.join(output_dir, f"results_{timestamp}.xml")

    with open(output_file, "wb") as output:
        runner = xmlrunner.XMLTestRunner(output=output)
        runner.run(suite)

