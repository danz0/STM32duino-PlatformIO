# STM32duino-Framework
STM32duino Framework for **PlatformIO 3.0**

Currently supported devices: 
* STM32F103Rx(R8, RB, RC, RE)

Device flashing: **Windows: serial only**

#### Quick & dirty installation:
* Install PlatformIO IDE;
* Clone this repo and rename folder to **stm32duino**;
* Place _stm32duino_ folder to _UserFolder/.platformio/packages_;
* Launch IDE and you should be able to see STM32 boards when creating new project.

##### Command line initialization:
Open terminal and write:
* pio init -b __BOARD_NAME__
* platformio run

##### **Notes:** 
* This installation is for official PlatformIO IDE: Atom. 
* _UserFolder_ is **%HOMEPATH%** on Windows or just C:\Users\Username...
* __BOARD_NAME__ can be f103r, f103rb, f103rc, f103re.
* PlatformIO 3.0 with Atom currently have a bug while trying to create new project, instead use command line initialization.
