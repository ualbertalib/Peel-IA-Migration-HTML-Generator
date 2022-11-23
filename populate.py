#!/usr/bin/python

import csv

with open('metadata2.csv', mode ='r')as file:
  #metadata = csv.reader(file)
  metadata = csv.DictReader(file)
  for line in metadata:
        print(line[])


#print(f"First line: {metadata[0]}")
