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
  - [Selecting Journals](#selecting-journals)
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

### Selecting Journals
Before running the program you need to specify the journals that you want to track. This can be done by editing either the [my_journals.xlsx](/data/my_journals.xlsx) spreadsheet. The current selection is the one that works best for me, so be free to change it according to your needs. To select the journals you want, go to the [top_journals.xlsx](data/top_journals.xlsx) and delete the lines corresponding to the undesired journals. Then rename it as *my_journals.xlsx* and overwrite the current file. The journals are ordered by their Repec rank.

The program [top_journals.py](/top_journals.py) can be used to get the top *n* journals. This can be done by running the following command:

```bash
python top_journals.py
```

It will automatically get the top 500 journals and store them in the [journals.json](/data/journals.json) file on the [data](/data) folder. The number of journals to be scraped can be changed by editing the variable *max_ranking* in the [top_journals.py](/top_journals.py) file.

## 🚀 Deployment <a name = "deployment"></a>

To run the program simply type

```bash
python get_articles.py
```

and the code will produce the [data/articles.json](/data/articles.json) file. This file contains the metadata for the most recent releases of the selected journals.

The number of most recent versions to be scraped can also be changed by editing the variable *n_months* in the [get_articles.py](/get_articles.py) file. The default value is 1, which collects all the papers published in the previous month. Setting it to -1 will collect all available articles. The variable *n_version* collects the *n* most recent versions of each journal. The default value is 1, which collects the most recent version of each paper. Setting it to -1 collects all available versions.

## 🤖 Automation <a name = "automation"></a>

I used this program to automatically get the latest versions of my desired top journals and add them to my task manager [Things](https://culturedcode.com/things/). This is done using Things` new Apple Shortcuts feature which I used to create [this shortcut](https://www.icloud.com/shortcuts/6a873d1662244c7d9fa959bfaf3bddd0). This tutorial is replicable in macOS only. 
To replicate it, first you need to create an automation to run this program every month. To do this, open the Automator app and create a new service. Then, add a Run Shell Script action and paste the following code:

```bash
python /path_to_repo/retrack/get_articles.py
shortcuts run "ReTrack" -i /path_to_repo/retrack/data/articles.json
```

Save this into your Automator iCloud folder. Then, open the Calendar app and create a new event and schedule it to repeat as you like. Finally, click *Alert > Custom*, select *Open File*, *Other* and find the Automator file you just created. This will run the program every time the event is triggered.

If you don't use Things, there is a version of this shortcut that exports that into a *Markdown* file. It can be found [here](https://www.icloud.com/shortcuts/0d680d0eabaf489e8c77c2e124e433f8). The markdown version can also be created from the [markdown_export.py](/markdown_export.py) file. To do this, change the Automator file to:

```bash
python /path_to_repo/retrack/get_articles.py
python /path_to_repo/retrack/markdown_export.py
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraping
- [IDEAS RePEc](https://ideas.repec.org) - Database
- [Apple Shortcuts](https://support.apple.com/en-us/HT208309) - Automation
- [Apple Automator](https://support.apple.com/en-us/HT201236) - Automation
- [Things](https://culturedcode.com/things/) - Task Manager

## ✍️ Authors <a name = "authors"></a>

- [@joseparreiras](https://github.com/joseparreiras) - Idea & Initial work