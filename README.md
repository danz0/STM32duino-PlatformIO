# STM32duino PlatformIO
STM32duino Platform for **PlatformIO 3.0**

Currently supported devices: 
* STM32F103Rx(R8, RB, RC, RE)
* STM32F103Cx(C8, CB)

Device flashing: **serial only**

#### Quick installation:
* Install PlatformIO CLI (or IDE, it will have CLI);
* Open PlatformIO CLI;
* Install platform by following command:

> platformio platform install https://github.com/ubis/STM32duino-PlatformIO/archive/master.zip

##### Command line initialization:
Open terminal and write:
* pio init -b __BOARD_NAME__
* platformio run

##### **Notes:** 
* This installation is for PlatformIO 3.0.
* __BOARD_NAME__ can be f103r, f103rb, f103rc, f103re, f103c8, f103cb.
* PlatformIO 3.0 with Atom on Windows, currently have a bug while trying to create new project, instead use command line initialization.
