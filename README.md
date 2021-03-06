#  python3, back-end & full stack
Solutions for python, back-end & full stack competencies assigned in EvolveU's [Full Stack Developer Program](https://www.evolveu.ca/program).


&nbsp;
&nbsp;


## Installation

__Prerequsites:__ [Git](https://git-scm.com) and [pipenv](https://github.com/pypa/pipenv) installed

Each folder (`Comp200, Comp220, Comp230, Comp240, Comp250`) contains a seperate python3-based project.

After cloning the repo., in order to run a project, one would have to enter the project's folder, use `pipenv` to install all required dependencies & re-create the virtual environment for the project, and then run the python3 scripts therein from within the virtual environment.

__General installation instructions:__
```bash
# Clone repository
$ git clone https://github.com/OmarHussainX/evolveu-python.git

# Enter folder for a specific project, e.g.
$ cd evolveu-python/Comp200

# Install dependencies, re-creating the virtual environment specified in `pipfile.lock`
$ pipenv install --ignore-pipfile

# OR to install all dependencies (regular and development dependencies)
$ pipenv install --dev

# Activate the virtual environment just created
$ pipenv shell

# Run scripts (from inside the virtual environment)
$ python tax_calc.py
$ python format_email.py
```


&nbsp;
&nbsp;


## Usage

Varies quite a bit depending on the project... Until this README is further developed, the best way to understand the purpose of a given project would be to review the corresponding assignment. Then the solution developed for the project will make sense.

* [Comp 200 - Python Logic](#comp-200---python-logic)
* [Comp 220 - Python File IO](#comp-220---python-file-io)
* [Comp 230 - Python Excel](#comp-230---python-excel)
* [Comp 240 - Python Flask](#comp-240---python-flask)
* [Comp 250 - Full Stack](#comp-250---full-stack)


&nbsp;

## Comp 200 - Python Logic
_[Comp 200 - Python Logic](Comp200/Comp%20200%20-%20Python%20Logic.pdf)_


&nbsp;


## Comp 220 - Python File IO
_[Comp 220 - Python File IO](Comp220/Comp%20220%20-%20Python%20File%20IO.pdf)_



&nbsp;


## Comp 230 - Python Excel
_[Comp 230 - Python Excel](Comp230/Comp%20230%20-%20Python%20Excel.pdf)_


&nbsp;


## Comp 240 - Python Flask
_[Comp 240 - Python Flask](Comp240/Comp%20240%20-%20Python%20Flask.pdf)_

__NOTE:__ This project contains two subfolders: one for the front-end, one for the back-end, each of which need to be run independently.

&nbsp;


## Comp 250 - Full Stack
_[Comp 250 - Full Stack](Comp250/Comp%20250%20-%20Full%20Stack.pdf)_

__NOTE:__ This project contains two subfolders: one for the front-end, one for the back-end, each of which need to be run independently.
