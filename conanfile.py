#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import shutil

from conans import ConanFile, tools


class TestPackageConan(ConanFile):
    name = "qt-module-svg"
    version = "5.9.6"
    settings = "os", "compiler", "build_type", "arch"
    generators = "qt"

    requires = "Qt/{0}@bincrafters/stable".format( "5.9.6")    
    generators = "virtualenv"

   

    def source(self):
        url = "http://download.qt.io/official_releases/qt/{0}/{1}/submodules/qtsvg-opensource-src-{1}"\
        .format(self.version[:self.version.rfind('.')], self.version)
        
        if tools.os_info.is_windows:
            tools.get("%s.zip" % url)
        elif sys.version_info.major >= 3:
            tools.get("%s.tar.xz" % url)
        else:  # python 2 cannot deal with .xz archives
            self.run("wget -qO- %s.tar.xz | tar -xJ " % url)

        shutil.move("qtsvg-opensource-src-%s" % self.version, "qtsvg")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("strawberryperl/5.26.0@david/testing")
        if self.settings.compiler == "Visual Studio":
            self.build_requires("jom_installer/1.1.2@bincrafters/stable")

   
    def build(self):
        tools.mkdir("qmake_folder")
        with tools.chdir("qmake_folder"):
            self.output.info("Building with qmake")

            def _qmakebuild():
                args = [self.build_folder + "/qtsvg/qtsvg.pro"]
                value = os.getenv('CC')
                if value:
                    args += ['QMAKE_CC=' + value,
                             'QMAKE_LINK_C=' + value,
                             'QMAKE_LINK_C_SHLIB=' + value]

                value = os.getenv('CXX')
                if value:
                    args += ['QMAKE_CXX=' + value,
                             'QMAKE_LINK=' + value,
                             'QMAKE_LINK_SHLIB=' + value]

                qmake_cmd =  "qmake %s  " % " ".join(args)   
                print(qmake_cmd)         
                self.run(qmake_cmd, run_environment=True)
                if tools.os_info.is_windows:
                    if self.settings.compiler == "Visual Studio":
                        self.run("jom")
                    else:
                        self.run("mingw32-make")
                else:
                    self.run("make")

            if self.settings.compiler == "Visual Studio":
                with tools.vcvars(self.settings):
                    _qmakebuild()
            else:
                _qmakebuild()
    
   
    def _test_with_qmake(self):
        self.output.info("Testing qmake")
        if tools.os_info.is_windows:
            bin_path = str(self.settings.build_type).lower()
        elif tools.os_info.is_linux:
            bin_path = "."
        else:
            bin_path = os.path.join("test_package.app", "Contents", "MacOS")
        bin_path = os.path.join("qmake_folder", bin_path)
        shutil.copy("qt.conf", bin_path)
        self.run(os.path.join(bin_path, "test_package"))

    def test(self):
        if not tools.cross_building(self.settings):
            self._test_with_qmake()

    def package(self):
        self.copy("*", src=self.build_folder +"/qmake_folder" )

    def package_info(self): 
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)