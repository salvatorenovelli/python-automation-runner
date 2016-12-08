# Python Automation Runner


With this runner, I'd like to provide python users with a portable<sup>1</sup> python environment that exposes a basic but powerful set of API to write automation and assertion scripts to create testing scenarios for **native/graphic** applications.
The environment will also function as a script `runner`, allowing the user to start and stop their script using windows hotkey. *(this may be more of a script debug feature)*

The main target are:
- provide a portable<sup>1</sup> environment to run python scripts via hotkey
- provide API in a domain language familiar to business/ testers/ QA to allow better business integration and easy transition to BDD.



###Example testing script:
```python

import logging
import time

import user_interaction as ui


logging.info("External script loaded")


def main_loop():

    logging.info("Current cursor position is: %s", str(ui.get_cursor_pos()))
    logging.info("Current foreground application executable is: %s", str(ui.get_foreground_window_executable()))

    logging.info("Clicking...")
    ui.click(100, 100)
    time.sleep(10)    

```

##Description

The runner can be packaged as a windows executable (instructions below) that load, interpret, run and terminate an external python script via hotkeys. 

If the external script will expose a function named `main_loop`, it will be run in loop indeed when `CTRL-ALT-M` will be pressed and **terminated** when  `CTRL-ALT-J` is pressed.

The runner is also resilient to syntax/runtime errors in the external script, allowing the user to modify it and reload via hotkey without having to restart the runner.

**NOTE: If you need to automate web application do NOT use this, please use [Selenium][2].**

##Usage

###Building the executable
    python setup.py build
This will create a `build/exe.win<PLATFORM>-<PYTHON_VERSION>` folder that will contain the `runner.exe`

###Running the runner...

    runner.exe myscript.py

###Starting and stopping the loop

- `CTRL-ALT-M` to **start** the `main_loop`
- `CTRL-ALT-J` to **stop** the `main_loop`


###Roadmap: Future features

- Introduce more interaction API
- Allow user to bundle custom libraries into the executable or to load them from the custom script location
- Allow image matching to assert visual behaviour
  - Support dry run to to let the user capture the expected behaviour without having to capture the expected image manually
- Support Gherkin with behave
- Control the tested environment via REST to allow automations that involve multiple machines
- Reporting



<sup>1</sup> *That can be copy/pasted in the target environment.*



  [1]: http://ahkscript.org/
  [2]: http://www.seleniumhq.org/
