# Peel-IA-Migration-HTML-Generator
* Inception: Nov, 2022
* This exists because Natasha asked for help with a python project to use a spreadsheet to template-out fragmented HTML, part of the Peel migration to the Internet Archive
* [Natasha's Sandbox mock-up](https://library.ualberta.ca/sandbox/natasha/peel/newspapers)
* For instance, [Search IA for "The Advertiser and Central Alberta News"](https://archive.org/search.php?query=the%20advertiser%20and%20central%20alberta%20news)
* Python Reference: [Reading CVS Files in Python](https://www.geeksforgeeks.org/reading-csv-files-in-python/)


Requirements:
  - python3
  - A .CSV with the following headers in the first row:
```
"Primary Access" "Q code" "IA URL" "Peel URL" "Pub start" "Pub end" "Related items" "Display title" "Coverage-Province" "Language" "Coverage-City1" "Notes"
```

Usage:
  - Pull down this repo for the script ```populate.py```
  - Bring the script ```populate.py``` and the desired .CSV into the same directory
  - While within the script and CSV directory run the script from the command line as follows:
```python3 populate.py PROVIDED_CSV.csv```

