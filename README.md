# STM32duino-Framework
STM32duino Framework for PlatformIO

Currently supported devices: 
* STM32F103Rx(R8, RB, RC, RE)

Device flashing: **Windows: serial only**

#### Quick & dirty installation:
* Install PlatformIO IDE;
* Launch IDE, install **atmelsam** platform or set up new Arduino Due board then close IDE;
* Clone this and https://github.com/rogerclarkmelbourne/Arduino_STM32 repo;
* Place _Arduino_STM32_ folder **contents** to _framework-stm32duino_ folder;
* Copy _framwork-stm32duino_ folder to _UserFolder/.platformio/packages_;
* Copy _platformio_ folder **contents** to _UserFolder/.atom/packages/platformio-ide/penv/Lib/site-packages/platformio_
* Edit _UserFolder/.platformio/packages/appstate.json_ as shown below.

Open _appstate.json_ with text editor and write into _"installed_platforms"_: **"stm32duino"**.

Next, find the place of _framework-arduinosam_, it should be in _installed_packages_.  
Write _"framework-stm32duino": {"version": 15, "time": 1465466499}_ .
  
Example of _appstate.json_ file: https://github.com/ubis/STM32duino-Framework/blob/master/appstate.json
##### **Notes:** 
* This installation is for official PlatformIO IDE: Atom. 
* _UserFolder_ is **%HOMEPATH%** on Windows or just C:\Users\Username...
