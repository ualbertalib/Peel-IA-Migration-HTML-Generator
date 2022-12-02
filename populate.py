#!/usr/bin/python

import csv

with open('metadata2.csv', mode ='r')as file:
  #metadata = csv.reader(file)
  metadata = csv.DictReader(file)
  for line in metadata:
        print(f'<!--{line["Display title"]}-->')
        print(f'<div class="card card-body item {line["Coverage-Province"]} {line["Language"]} {line["Coverage-City1"]>')
        print(f'\t<h5><a href="https://archive.org/details/{line["Q code"]}">{line["Display title"]}</a></h5>')
        print(f'\t<p class="ml-2 mb-0">{line["Pub start"]} to {line["Pub end"]}</p> ')
        print('\t<hr/>')
        print('<div class="small px-2 py-1">')
        print(f'\t<p>{line["Notes"]}</p>')
        print(f'<p>{line["Related items"]}</p>')
        print('\t</div>')
        print('</div>')

        print()

