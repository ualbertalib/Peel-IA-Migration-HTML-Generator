#!/usr/bin/env python3

import sys
import csv

# Hardcoding file argument from sys.argv[1]

if len(sys.argv) < 2:
  print('Wrong number of arguments. You need to provide a filename')
  sys.exit() 
  
# Hardcoding file argument from sys.argv[1]
with open(sys.argv[1], mode ='r') as file:
  metadata = csv.DictReader(file)
  for line in metadata:
    print(f'''
      <!--{line["Display title"]}-->
      <div class="card card-body item {line["Coverage-Province"]} {line["Language"]}">
        <h5><a href="https://archive.org/details/{line["Q code"]}">{line["Display title"]}</a></h5>
        <p class="ml-2 mb-0">{line["Pub start"]} to {line["Pub end"]}</p>
        <hr/>
        <div class="small px-2 py-1">
        <p>{line["Notes"]}</p>
        <p>{line["Related items"]}</p>
        </div>
      </div>
    ''')
