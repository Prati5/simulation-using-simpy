
# Container Terminal Simulation

This project is a basic simulation of a container terminal using SimPy. It models trucks arriving at the terminal, loading and unloading containers, and leaving the terminal.

The simulation will run for 50 time units by default. You can adjust the simulation time by modifying the `until` parameter in the `env.run(until=50)` line in `main.py`.

## Simulation Results

After running the simulation, the program will print the total number of containers loaded and unloaded during the simulation.

**Pre-Requisites**

Pycharm
Ubntu/Windows
Python3.10
Virtual environment

**Installing the Project**

Create the virtual environments using python3 -m venv environment_name
Activate the venv by running this: source {your env name}/bin/activate
Intall the required packages mentioned in the requirements folder pip install -r requirements/requirements.txt

**Run the project**
To run the simulation, execute the simulation.py

Note:

To avoid commit python compiled files(.pyc) files please add these into .gitignore file *.pyc

Before commit the code please use pep8 check. please refer below url:

https://www.python.org/dev/peps/pep-0008/ we can use PyCharm(editor) Code -> Inspect Code utility for pep8 guideline.
