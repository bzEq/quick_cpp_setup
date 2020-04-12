#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


class ArgumentParser(object):
    @staticmethod
    def get_configuration(argv):
        parser = argparse.ArgumentParser(description="Quick C++ Setup")
        parser.add_argument('--base_directory', default='.')
        parser.add_argument('--project_name', required=True)
        parser.add_argument('--without_googletest', action='store_true')
        parser.add_argument('--without_clang_format', action='store_true')
        parser.add_argument('--without_yapf', action='store_true')
        parser.add_argument(
            '--googletest_path', default='third_party/googletest')
        parser.add_argument('--author', default='Kai Luo <gluokai@gmail.com>')
        configuration = parser.parse_args(argv)
        return configuration
