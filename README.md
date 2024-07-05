# Saldo job interview task

## Task Description

This project involves writing an automated test to [xe.com currency widget](https://www.xe.com/currencytables). The goal is to ensure that the historical currency rate widget works as expected.

## Implementation description

Automated tests were implemented with Selenium on python.

Tests are using unittest library.

Currently the tests are able to be run on both Chrome and Firefox.

Results are output into test-reports folder in XML format.

## Steps to Launch the Python Script

To run the automated tests, follow these steps:

1. **Clone the repository:**

   ```bash
   https://github.com/jokubaskon/saldo_task.git
   cd saldo_task
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure you have both Firefox and Chrome installed**

   If one of them is missing, make sure to run the tests with one of these flags:

   ```
   --firefox

   or

   --chrome
   ```

4. **Run the automated test:**

   ```bash
   python run_tests.py # Runs all of the tests
   ```

   ```bash
   python run_tests.py --firefox # Runs tests on firefox
   ```

   ```bash
   python run_tests.py --chrome # Runs tests on chrome
   ```
