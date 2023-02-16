<h1 align="center">💡 ReTrack</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/joseparreiras/retrack.svg)](https://github.com/joseparreiras/retrack/issues)
![Last Commit](https://img.shields.io/github/last-commit/joseparreiras/retrack)
![Language](https://img.shields.io/github/languages/top/joseparreiras/retrack)
![Git Forks](https://img.shields.io/github/forks/joseparreiras/retrack?label=Fork)

</div>

---

<p align="center"> This is an automation designed to track the publications of top economic journals using IDEAS RePEc database.
    <br> 
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
- [🎈 Usage ](#-usage-)
  - [✅ Selecting Journals](#-selecting-journals)
    - [1. Selecting a range of journals by their RePEc rank:](#1-selecting-a-range-of-journals-by-their-repec-rank)
    - [2. Selecting a list of journals by their Repec rank:](#2-selecting-a-list-of-journals-by-their-repec-rank)
  - [❓ Other Arguments](#-other-arguments)
- [🤖 Automation ](#-automation-)
- [⛏️ Built Using ](#️-built-using-)
- [✍️ Authors ](#️-authors-)

## 🧐 About <a name = "about"></a>

This program uses the BeautifulSoup and Requests modules to scrape the RePEc website for the top journals and downloads the metadata for their most recent releases. It then stores this data into a *.json* file that can be used for other automations. The program is designed to be run on a monthly basis to ensure that the data is up to date. Up to the current date, Ideas update its database on the 2nd day of every month.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/joseparreiras/retrack 
cd retrack
```

To run the program, you first need to make sure your system satisfies the module requirements. This can be done using the following command:

```bash
pip install -r requirements.txt
```

The modules that are not pre-installed will be installed automatically.

## 🎈 Usage <a name="usage"></a>

The documentation for the main program can be accessed by running the help command on the terminal:

```bash
python get_articles.py -h
```

Which will generate the following output:

```
usage: get_articles.py [-h] [--input INPUT] [--list] [--range] [--output OUTPUT] [--n_months N_MONTHS] [--n_volumes N_VOLUMES] rankings [rankings ...]

positional arguments:
  rankings              journal rankings

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to excel input file
  --list, -l            get a list of journals
  --range, -r           get a range of journals
  --output OUTPUT, -o OUTPUT
                        path to output file
  --n_months N_MONTHS, -m N_MONTHS
                        number of months to get
  --n_volumes N_VOLUMES, -v N_VOLUMES
                        number of volumes to get
````

The file [journals.xlsx](data/journals.xlsx) on the [data](/data) folder contains the list of the top 500 journals according to the RePEc ranking. This ranking is used to select the journals that will be downloaded. When the program is run, it will automatically get the top 500 journals and store them in the [articles.json](/data/articles.json) file on the [data](/data) folder. The program can be run using the following command on the terminal:

```bash
python get_articles.py data/journals.xlsx
```

### ✅ Selecting Journals

Selection of journals is made by passing the *rankings* argument to the command above. There are three options for selecting journals:
#### 1. Selecting a range of journals by their RePEc rank:

Passing 2 arguments along with the option `--range` or `-r` will select the journals from the first to the second argument. For example, running the following command:
```bash
python get_articles.py start_rank end_rank -r
```
Passing 1 argument along with the option `--range` or `-r` will select the journals from the first to the `end_rank`. For example, running the following command:
```bash
python get_articles.py end_rank -r
```

#### 2. Selecting a list of journals by their Repec rank:

Passing a list of arguments along with the option `--list` or `-l` will select the journals with the specified ranks. This list must be separated by spaces and the *list* keyword (which necessarily comes at last) is used to indicate that the ranks are to be interpreted as a list. For example, running the following command:
```bash
python get_articles.py  rank1 rank2 rank3 ... -l
```
The `-list` option cannot be used together with the `-range` option and is taken as the default option if no option is specified. Therefore the above command is equivalent to running:
```bash
python get_articles.py rank1 rank2 rank3 ...
```

### ❓ Other Arguments  

The program also takes the following optional arguments:

- `--input` or `-i`: This argument is used to specify the path to the source excel file. The default value is `data/journals.xlsx`.
- `--output` or `-o`: This argument is used to specify the path to the output JSON file. The default value is `data/articles.json`.
- `--n_months` or `-m`: This argument is used to specify the number of months to get. The default value is 1. Setting it to -1 will get all the articles.
- `--n_volumes` or `-v`: This argument is used to specify the number of volumes to get. The default value is 3. Setting it to -1 will get all the volumes.

That can be used in any combination. For example, to get the articles from the last 12 months considering the last 6 volumes of each journal and store them in the "data/foo.json" file, run:

```bash
python get_articles.py -o data/foo.json -m 12 -v 6
```

The default input file is [journals.xlsx](data/journals.xlsx) which contains the top 500 journals according to the RePEc ranking. This file is obtained by running the [top_journals.py](/top_journals.py) program. This program can be used to get the top *N* journals. This can be done by running the following command:

```bash
python top_journals.py N
```
## 🤖 Automation <a name = "automation"></a>

I used this program to automatically get the latest versions of my desired top journals and add them to my task manager [Things](https://culturedcode.com/things/). This is done using Things` new Apple Shortcuts feature which I used to create [this shortcut](https://www.icloud.com/shortcuts/6a873d1662244c7d9fa959bfaf3bddd0). This tutorial is replicable in macOS only. 
To replicate it, first you need to create an automation to run this program every month. To do this, open the Automator app and create a new service. Then, add a Run Shell Script action and paste the following code:

```bash
python /path_to_repo/retrack/get_articles.py other_arguments
shortcuts run "ReTrack" -i /path_to_repo/retrack/data/articles.json
```

Save this into your Automator iCloud folder. Then, open the Calendar app and create a new event and schedule it to repeat as you like. Finally, click *Alert > Custom*, select *Open File*, *Other* and find the Automator file you just created. This will run the program every time the event is triggered.

If you don't use Things, there is a version of this shortcut that exports that into a *Markdown* file. It can be found [here](https://www.icloud.com/shortcuts/0d680d0eabaf489e8c77c2e124e433f8). The markdown version can also be created from the [markdown_export.py](/markdown_export.py) file. To do this, change the Automator file to:

```bash
python /path_to_repo/retrack/get_articles.py other_arguments
python /path_to_repo/retrack/markdown_export.py /path_to_repo/retrack/data/articles.json
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping
- [IDEAS RePEc](https://ideas.repec.org) - Database
- [Apple Shortcuts](https://support.apple.com/en-us/HT208309) - Automation
- [Apple Automator](https://support.apple.com/en-us/HT201236) - Automation
- [Things](https://culturedcode.com/things/) - Task Manager

## ✍️ Authors <a name = "authors"></a>

- [@joseparreiras](https://github.com/joseparreiras) - Idea & Initial work