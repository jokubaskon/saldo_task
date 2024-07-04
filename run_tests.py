import unittest
import xmlrunner
import os
from datetime import datetime

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests")

    output_dir = 'test-reports'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    output_file = os.path.join(output_dir, f'results_{timestamp}.xml')

    with open(output_file, 'wb') as output:
        runner = xmlrunner.XMLTestRunner(output=output)
        runner.run(suite)