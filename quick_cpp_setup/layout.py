#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import string

gtest_BUILD = """\
cc_library(
    name="main",
    srcs=glob(
        [
            "googletest/src/*.cc",
            "googletest/src/*.h",
            "googletest/include/gtest/**/*.h",
            "googlemock/src/*.cc",
            "googlemock/include/gmock/**/*.h",
        ],
        exclude=[
            "googletest/src/gtest-all.cc",
            "googletest/src/gtest_main.cc",
            "googlemock/src/gmock-all.cc",
            "googlemock/src/gmock_main.cc",
        ]),
    hdrs=glob([
        "googletest/include/gtest/*.h",
        "googlemock/include/gmock/*.h",
    ]),
    includes=[
        "googlemock",
        "googlemock/include",
        "googletest",
        "googletest/include",
    ],
    linkopts=["-pthread"],
    visibility=["//visibility:public"],
)

cc_library(
    name="gtest_main",
    srcs=[
        "googlemock/src/gmock_main.cc",
    ],
    deps=["main"],
    visibility=["//visibility:public"],
)
"""

WORKSPACE = string.Template("""\
new_local_repository(
    name="gtest",
    build_file="gtest.BUILD",
    path="$googletest_path",
)
""")

CLANG_FORMAT = """\
BasedOnStyle: LLVM
SortIncludes: true
AlwaysBreakTemplateDeclarations: true
"""

YAPF = """\
[style]
based_on_style = pep8
"""


class Builder(object):

    BASIC_LAYOUT = [
        "include",
        "include/$project_name",
        "lib",
        "tools",
        "unittests",
    ]

    def __init__(self, configuration):
        self.configuration = configuration
        self.project_root = os.path.join(configuration.base_directory,
                                         configuration.project_name)

    def add_googletest(self):
        with open(os.path.join(self.project_root, "WORKSPACE"), "w") as f:
            f.write(
                WORKSPACE.safe_substitute(
                    googletest_path=self.configuration.googletest_path))
        with open(os.path.join(self.project_root, "gtest.BUILD"), "w") as f:
            f.write(gtest_BUILD)
        return True

    def add_clang_format(self):
        with open(os.path.join(self.project_root, ".clang-format"), "w") as f:
            f.write(CLANG_FORMAT)
        return True

    def add_yapf(self):
        with open(os.path.join(self.project_root, ".style.yapf"), "w") as f:
            f.write(YAPF)
        return True

    def build(self):
        if os.path.exists(self.project_root):
            logging.error(
                "Project %s already exists" % self.configuration.project_name)
            return False
        os.makedirs(self.project_root)
        for item in self.BASIC_LAYOUT:
            try:
                tmp = string.Template(item).safe_substitute(
                    project_name=self.configuration.project_name)
                d = os.path.join(self.project_root, tmp)
                os.makedirs(d)
            except Exception as e:
                logging.exception("os.makedirs")
                return False
        if not self.configuration.without_googletest:
            ok = self.add_googletest()
            if not ok:
                return False
        if not self.configuration.without_clang_format:
            ok = self.add_clang_format()
            if not ok:
                return False
        if not self.configuration.without_yapf:
            ok = self.add_yapf()
            if not ok:
                return False
        return True
