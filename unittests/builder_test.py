#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import os
import sys
import unittest

from quick_cpp_setup.commandline import ArgumentParser
from quick_cpp_setup.layout import Builder


class BuilderTest(unittest.TestCase):
    def test_build_smoketest(self):
        with tempfile.TemporaryDirectory() as d:
            argv = [
                '--base_directory',
                d,
                '--project_name',
                'wtf',
            ]
            self.assertTrue(
                Builder(ArgumentParser.get_configuration(argv)).build())


if __name__ == '__main__':
    unittest.main()
