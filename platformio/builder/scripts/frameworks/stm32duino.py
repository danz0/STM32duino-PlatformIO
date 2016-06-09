# Copyright 2014-2016 Ivan Kravets <me@ikravets.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
STM32duino

STM32duino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of STM32 boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://www.stm32duino.com
"""

from os import listdir, walk
from os.path import isdir, isfile, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

BOARD_OPTS = env.get("BOARD_OPTIONS", {})
BOARD_BUILDOPTS = BOARD_OPTS.get("build", {})
BOARD_CORELIBDIRNAME = BOARD_BUILDOPTS.get("core")

#
# Determine framework directory
# based on development platform
#

if "stm32f103" in BOARD_BUILDOPTS.get("mcu", ""):
    PLATFORMFW_DIR = join("$PIOPACKAGES_DIR", "framework-stm32duino", "STM32F1")
    
env.Prepend(
    CPPPATH=[
            join("$PLATFORMFW_DIR", "system", "libmaple"),
            join("$PLATFORMFW_DIR", "system", "libmaple", "include"),
            join("$PLATFORMFW_DIR", "system", "libmaple", "usb", "stm32f1"),
            join("$PLATFORMFW_DIR", "system", "libmaple", "usb", "usb_lib")
        ],

    LIBPATH=[
        join("$PLATFORMFW_DIR", "cores", "${BOARD_OPTIONS['build']['core']}"),
        join("$PLATFORMFW_DIR", "variants", "${BOARD_OPTIONS['build']['variant']}"),
        join("$PLATFORMFW_DIR", "variants", "${BOARD_OPTIONS['build']['variant']}", "ld")
    ]
)

env.Replace(PLATFORMFW_DIR=PLATFORMFW_DIR)

#
# Base
#

ARDUINO_VERSION = int(open(join(env.subst("$PIOPACKAGES_DIR"), "framework-stm32duino", "version.txt")).read().replace(".", "").strip())
ARDUINO_USBDEFINES = ["ARDUINO=%d" % ARDUINO_VERSION]

env.Append(
    CPPDEFINES=ARDUINO_USBDEFINES,
    CPPPATH=[join("$BUILD_DIR", "FrameworkArduino")]
)

#
# Target: Build Core Library
#

libs = []

if "variant" in BOARD_BUILDOPTS:
    env.Append(
        CPPPATH=[join("$BUILD_DIR", "FrameworkArduinoVariant")]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join("$PLATFORMFW_DIR", "variants", "${BOARD_OPTIONS['build']['variant']}")
    ))

envsafe = env.Clone()

libs.append(envsafe.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join("$PLATFORMFW_DIR", "cores", "${BOARD_OPTIONS['build']['core']}")
))

env.Prepend(LIBS=libs)
