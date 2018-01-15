#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import string
import datetime

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

BSD = string.Template("""\
Copyright (c) $year $author. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""")


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
        self.add_bsd()
        return True

    def add_bsd(self):
        with open(os.path.join(self.project_root, "LICENSE"), "w") as f:
            now = datetime.datetime.now()
            content = BSD.substitute({
                "year": str(now.year),
                "author": self.configuration.author,
            })
            f.write(content)
