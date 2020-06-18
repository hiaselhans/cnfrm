#!/bin/env python

import unittest
import sys

loader = unittest.TestLoader().discover("tests", "test*.py")

test_results = unittest.TextTestRunner(verbosity=0).run(loader)

#sys.exit(not test_results.wasSuccessful())