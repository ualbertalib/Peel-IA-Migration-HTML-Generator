#!/usr/bin/env python3

import sys
import csv
import re
import logging

logger = logging.getLogger()

urls = {}
def getUrl(shortCode):
  if shortCode in urls:
    return urls[shortCode]

# Hardcoding file argument from sys.argv[1]
if len(sys.argv) < 2:
  print('Wrong number of arguments. You need to provide a filename')
  sys.exit() 
  
# Hardcoding file argument from sys.argv[1]
with open(sys.argv[1], mode ='r') as file:
  metadata = csv.DictReader(file)
  
  for line in metadata:
    if line["Primary Access"] == "IA":
      urls[line["Q code"]] = line["IA URL"]
    elif line["Primary Access"] == "Peel":
      urls[line["Q code"]] = line["Peel URL"]
  file.seek(0)

  for line_count, line in enumerate(metadata):
    if line_count == 0:
      continue
    short_code_array = re.findall(r'<b>(.*?)\</b>', line["Related items"])
    for related_item_index, related_item in enumerate(line["Related items"].split("<br>")):
      if '<b>' not in related_item and related_item:
        short_code_array.insert(related_item_index, None)

    # Here we link to the matching shortcode inside bold tag. Change regex to
    # (<i>.*?<\/i>) if we just want to link the title
    title_array = re.findall(r'<i>(.*?)<\/i>', line["Related items"])
    matching_url_array = list(map(getUrl, short_code_array))
    related_items_field = line["Related items"]
    if (len(title_array) == len(matching_url_array)):
      for i, match in enumerate(matching_url_array):
        related_items_field_regex = r'(<b>.*?<i>)' + re.escape(title_array[i]) + r'(<\/i>)'
        replacing_title = title_array[i]
        if match:
          replacing_title = f"<a href=\"{matching_url_array[i]}\">{title_array[i]}</a>"
          
        related_items_field = re.sub(related_items_field_regex, replacing_title, related_items_field)

    else:
      logging.error(f"Links on line {line_count+1} do not match on 'Related items' column")

    publication_range = ''
    if line["Pub start"]:
      publication_range = line["Pub start"]
    if line["Pub end"]:
      publication_range += f' to {line["Pub end"]}'

    print(f'''
      <!--{line["Display title"]}-->
      <div class="card card-body item {line["Coverage-Province"]} {line["Language"]} {line["Coverage-City1"]}">
        <h5><a href="{urls[line["Q code"]]}">{line["Display title"]}</a></h5>
        <p class="ml-2 mb-0">{publication_range}</p>
        <hr/>
        <div class="small px-2 py-1">
        <p>{line["Notes"]}</p>
        <p>{related_items_field}</p>
        
        </div>
      </div>
    ''')
