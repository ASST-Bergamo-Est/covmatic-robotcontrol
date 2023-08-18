Covmatic Robotstation
=====================
A *[covmatic-station](https://pypi.org/project/covmatic-stations/)* extension package to enable the use of robotic arm with Opentrons OT2 pipetting robot.

> [!WARNING]
> This is a development program and not ready for production-use.
> This is part of a project in development.

> [!IMPORTANT]
> This package is part of an integrated system. You can find the full documentation
> of the system here: https://asst-bergamo-est.github.io/covmatic-covidseq-guide/


## Table of Contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Setup](#setup)
* [Execution](#execution)
* [Calibration](#calibration)
* [Development](#development)
* [Testing](#testing)
* [Publish](#publish)


## Introduction

**covmatic-robotstation** is an extension package build upon *[covmatic-station](https://pypi.org/project/covmatic-stations/)* base 
package. It enables a Covmatic *station* to talk with a *covmatic-robotmanager* instance to 
request plate transfer action like pick up, drop off plate.

Each *station* should be an instance of *RobotStationABC* abstract class: it contains
helper functions to correctly handle plate operations and *robotmanager* API.

Multiple *stations* can talk with the same instance of *robotmanager* in order to build a
coordinated robotic system.

For more information please go to the [Covmatic-Covidseq Guide](https://asst-bergamo-est.github.io/covmatic-covidseq-guide/)

## Installation

You can [install the Covmatic Robotstation via `pip`](https://pypi.org/project/covmatic-robotstation):
```
<python> -m pip install covmatic-robotstation
```
Where `<python>` should be changed for the Python instance you wish to install the Robotmanager onto. We will be following this convention for all the next instructions. 

## Setup

This package does not need any setup. Configurations are passed to class constructor during object creation.

## Execution

As an extension package of *covmatic-stations*, to execute a RobotStation instance you've to first create a class
child of **RobotStationABC** abstract class in a Opentrons python protocol file.
The *RobotStationABC* **__init__** function accept three parameters to connect to the *RobotManager* instance:
- *ot_name*: the *machine name* that will identify the OT2 in RobotManager's calls
- *robot_manager_host*: the IP address of RobotManager server;
- *robot_manager_port*: the port on which the RobotManager is listening.

Because **Station** class needs at least the *_tiprack* property defined, you've to declare it;
than you should define a *body* function that will hold the effective protocol executed
```
from covmatic_robotstation.robot_station import RobotStationABC


class TestRobotStation(RobotStationABC):
    def _tipracks(self) -> dict:
        return {}
        
    def body(self):
        self.robot_pick_plate(slot="SLOT1", plate_name="TESTPLATE")
        self.robot_drop_plate(slot="SLOT2", plate_name="TESTPLATE")
        self.robot_trash_plate(pick_slot="SLOT1", trash_slot="TRASHSLOT1", plate_name="TRASHPLATE")


metadata = {'apiLevel': '2.7'}
station = TestRobotStation(ot_name="OTTEST", 
                           robot_manager_host=192.168.1.1,
                           robot_manager_port=5000)


def run(ctx):
    return station.run(ctx)
```
Then you can save this protocol file, upload it on the Opentrons OT2 (with Jupyter notebook or SSH/SCP) 
to a defined position (e.g. */var/lib/jupyter/notebooks/protocol.py*) 
and you can execute it in a shell with:
```
opentrons_execute /var/lib/jupyter/notebooks/protocol.py
```
Alternatively you can load the protocol from a PC with the [Opentrons App](https://opentrons.com/ot-app/).

In case of any error during plate transfer (e.g. RobotManager instance not reachable, plate not grabbed)
the protocol will pause asking the user to manually transfer the plate.

## Calibration

Each of the slot names called in protocol must be already calibrated on the RobotManager instance.
E.g. regarding the protocol listed above, these position should be calibrated in the RobotManager
(see *Calibration* section in [RobotManager documentation](https://pypi.org/project/covmatic-robotmanager/) for more information):
- machine: OTTEST
  - slot names: SLOT1, SLOT2
- machine: TRASH
  - slot names: TRASHSLOT1

## Development

If you want to develop the package follow these step:
1. check out the source code:
   ```
   git checkout https://github.com/ASST-Bergamo-Est/covmatic-robotstation.git
   ```
2. modify the code and update the version in *src/covmatic_robotstation/__init__.py*
3. build the code:
   ```
   hatch build
   ```
4. install locally with:
   ```
   pip install .
   ```
   or use the wheel created in the *dist* folder.

## Testing

The covmatic-robotstation source code comes with a handful of tests to check that the code is doing as expected. 
It has been developed using a Test Driven Development approach.
To execute tests and coverage report just launch:
```
hatch run cov
```

## Publish

To publish a new version of the package be sure the package is satisfying the testing step;
then use *git* to add and commit everything.
The last step is to create a tag for version *x.y.x* with:
```
git tag vx.y.x
```
and to commit the tag with: 
```
git push origin tag vx.y.x
```
The *GitHub workflow* will then build the package, check for installation and unit testing and then upload the wheel on *PyPI*.