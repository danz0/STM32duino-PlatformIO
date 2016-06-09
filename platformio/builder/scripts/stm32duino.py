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
    Builder for STM32 series of microcontrollers
"""

from os.path import basename, join

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Default,
                          DefaultEnvironment, SConscript)

from platformio.util import get_serialports


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621
    env.AutodetectUploadPort()
    upload_options = env.get("BOARD_OPTIONS", {}).get("upload", {})

    if not upload_options.get("disable_flushing", False):
        env.FlushSerialBuffer("$UPLOAD_PORT")

    before_ports = get_serialports()

    if upload_options.get("use_1200bps_touch", False):
        env.TouchSerialPort("$UPLOAD_PORT", 1200)

    if upload_options.get("wait_for_upload_port", False):
        env.Replace(UPLOAD_PORT=env.WaitForNewSerialPort(before_ports))

    # use only port name for BOSSA
    if "/" in env.subst("$UPLOAD_PORT"):
        env.Replace(UPLOAD_PORT=basename(env.subst("$UPLOAD_PORT")))


env = DefaultEnvironment()

env.Replace(
    UPLOADER=join("$PIOPACKAGES_DIR", "framework-stm32duino", "tools", "win", "serial_upload"),
    UPLOADERFLAGS=["$UPLOAD_PORT"],
    UPLOADCMD='"$UPLOADER" $UPLOADERFLAGS {upload.altID} {upload.usbID} $PROJECT_DIR\$SOURCES'
)

SConscript(env.subst(join("$PIOBUILDER_DIR", "scripts", "basearm.py")))

env.Append(

    CCFLAGS=[
        "--param", "max-inline-insns-single=500",
        "-MMD"
    ],

    CFLAGS=[
        "-std=gnu11"
    ],

    CXXFLAGS=[
        "-std=gnu++11",
        "-fno-threadsafe-statics"
    ],

    CPPDEFINES=[
        "USBCON"
    ],

    LINKFLAGS=[
        "-Wl,--check-sections",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        "-Wl,--warn-section-align",
        "$BUILD_DIR/FrameworkArduinoVariant/wirish/syscalls.o"
    ]
)

#
# Target: Build executable and linkable firmware
#

target_elf = env.BuildProgram()

#
# Target: Build the .bin file
#

if "uploadlazy" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.bin")
else:
    target_firm = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Print binary size
#

target_size = env.Alias("size", target_elf, "$SIZEPRINTCMD")
AlwaysBuild(target_size)

#
# Target: Upload by default .bin file
#

if env.subst("$BOARD") == "zero":
    upload = env.Alias(["upload", "uploadlazy"], target_firm, "$UPLOADCMD")
else:
    upload = env.Alias(["upload", "uploadlazy"], target_firm,
                       [BeforeUpload, "$UPLOADCMD"])

AlwaysBuild(upload)

#
# Setup default targets
#

Default([target_firm, target_size])
