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
    - [Selecting a range of journals by their Repec rank:](#selecting-a-range-of-journals-by-their-repec-rank)
    - [Selecting a list of journals by their Repec rank:](#selecting-a-list-of-journals-by-their-repec-rank)
  - [🗳️ Source File](#️-source-file)
- [🚀 Deployment ](#-deployment-)
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

The file [journals.xlsx](data/journals.xlsx) on the [data](/data) folder contains the list of the top 500 journals according to the RePEc ranking. This ranking is used to select the journals that will be downloaded. When the program is run, it will automatically get the top 500 journals and store them in the [articles.json](/data/articles.json) file on the [data](/data) folder. The program can be run using the following command on the terminal:

```bash
python get_articles.py data/journals.xlsx
```

### ✅ Selecting Journals

You can select the journals that you want in 3 different ways:

#### Selecting a range of journals by their Repec rank:
```bash
python get_articles.py data/journals.xlsx start_rank end_rank range
```
which will select the journals from the *start_rank* to the *end_rank*, or
```bash
python get_articles.py data/journals.xlsx end_rank range
```
which will select the journals from the first to the *end_rank*.

#### Selecting a list of journals by their Repec rank:
```bash
python get_articles.py data/journals.xlsx rank1 rank2 rank3 ... list
```
which will select the journals with the specified ranks. The ranks are separated by spaces and the *list* keyword (which necessarily comes at last) is used to indicate that the ranks are to be interpreted as a list.


### 🗳️ Source File
The source file can also be changed by parsing

```bash
python get_articles.py path/to/source_file *other_arguments
```

The original file [journals.xlsx](data/journals.xlsx) is obtained from running the [top_journals.py](/top_journals.py) program. This program can be used to get the top *n* journals. This can be done by running the following command:

```bash
python top_journals.py
```

It will automatically get the top 500 journals and store them on the [data](/data) folder. The number of journals to be scraped can be changed by entering an integer as an argument when running the program. For example, to get the top 1000 journals, run

```bash
python top_journals.py 1000
```
## 🚀 Deployment <a name = "deployment"></a>

The program can be run as explained in the [Usage](#usage) section. To run the program, simply run the following command on the terminal:

```bash
python get_articles.py path/to/source_file other_arguments
```

and the code will produce the [data/articles.json](/data/articles.json) file. This file contains the metadata for the most recent releases of the selected journals.

The number of most recent versions to be scraped can also be changed by editing the variable *n_months* in the [get_articles.py](/get_articles.py) file. The default value is 1, which collects all the papers published in the previous month. Setting it to -1 will collect all available articles. The variable *n_version* collects the *n* most recent versions of each journal. The default value is 3, which collects the 3 most recent version of each paper. Setting it to -1 collects all available versions.

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