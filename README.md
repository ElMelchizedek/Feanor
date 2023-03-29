# Feanor

Feanor is a web app built on PyFlask that provides the user with movie recommendations based upon the name of a film they input using machine-learning and the MovieLens dataset.

## Installation
This software has only been written for use on Arch Linux, and so the user is trusted to know how to convert any Arch or Linux-specific instructions to their preferred operating system.

The steps to install the software are simple.
You will first need to clone the repository:
```bash
git clone https://github.com/TheVerl/Feanor.git
cd Feanor
```
Make sure that you have Python updated to the latest version, and then use [pip](https://pip.pypa.io/en/stable/) to install the required dependencies:
```bash
pip install -r requirements.txt
```
You will then have to download and extract the latest MovieLens dataset into a new "data" subdirectory:
```bash
wget https://files.grouplens.org/datasets/movielens/ml-latest.zip
mkdir data/
unzip -q ml-latest.zip
mv ml-latest/* data/
```
Finally, run the data sorting script and wait until it finishes. It should take about 15 minutes, depending on your hardware:
```bash
python sortData.py
```

## Usage
Simply run Flask, open http://localhost:5000, input your film name and hit 'Select' and hopefully after a minute or two it will output a list of films along with why they would be a good fit for you. Note that the database is small, and many films listed in it do not have sufficient data to be considered by the ML algorithm. Also note that the form is case sensitive, so complex title names won't be inputed easily (e.g. you will have to enter "Star Wars: Episode V - The Empire Strikes Back", rather than just "The Empire Strikes Back"):
```bash
flask run
```