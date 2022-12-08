#!/usr/bin/env python3

import sys
import csv
import re
import logging

logger = logging.getLogger()

urls = {}

def get_url(short_code: any):
  if short_code in urls:
    return urls[short_code]

def process_urls(metadata: any):
  for line in metadata:
    if line["Primary Access"] == "IA":
      urls[line["Q code"]] = line["IA URL"]
    elif line["Primary Access"] == "Peel":
      urls[line["Q code"]] = line["Peel URL"]
  file.seek(0)

def get_publication_range(line: any):
  publication_range = ''
  if line["Pub start"]:
    publication_range = line["Pub start"]
  if line["Pub end"]:
    publication_range += f' to {line["Pub end"]}'
  return publication_range

if __name__ == '__main__':

  if len(sys.argv) < 2:
    logger.warning("Wrong number of arguments. You need to provide a filename. Example: %s filename.csv", sys.argv[0])
    sys.exit()
    
  # Hardcoding file argument from sys.argv[1]
  with open(sys.argv[1], mode ='r', encoding="utf-8") as file:
    metadata = csv.DictReader(file)
    
    # Gather all the urls we will need based on the "Primary Access" column in CSV file.
    process_urls(metadata)

    for line_count, line in enumerate(metadata):
      # We dont process the headers column in the CSV file
      if line_count == 0:
        continue
      short_code_array = re.findall(r'<b>(.*?)\</b>', line["Related items"])
      for related_item_index, related_item in enumerate(line["Related items"].split("<br>")):
        # If we dont have a <b> tag insert just the title
        if '<b>' not in related_item and related_item:
          short_code_array.insert(related_item_index, None)

      # Here we link to the matching shortcode inside bold tag. Change regex to
      # (<i>.*?<\/i>) if we just want to link the title
      title_array = re.findall(r'<i>(.*?)<\/i>', line["Related items"])
      matching_url_array = list(map(get_url, short_code_array))
      related_items_field = line["Related items"]

      # Check if all titles have corresponding links which are marked with
      # shortcodes defined in the <b></b> tags, otherwise leave related_items_field as it was
      if (len(title_array) == len(matching_url_array)):
        for i, match in enumerate(matching_url_array):
          related_items_field_regex = r'(<b>.*?<i>)' + re.escape(title_array[i]) + r'(<\/i>)'
          replacing_title = title_array[i]
          if match:
            replacing_title = f"<a href=\"{matching_url_array[i]}\">{title_array[i]}</a>"

          related_items_field = re.sub(related_items_field_regex, replacing_title, related_items_field)

      else:
        logging.error("Links on line %s do not match on 'Related items' column", line_count+1)

      # Make sure we add the correct publication date range if "Pub start" and "Pub end" exist or not
      publication_range = get_publication_range(line)

      print(f'''
        <!--{line["Display title"]}-->
        <div class="card card-body item {line["Coverage-Province"]} {line["Language"]} {line["Coverage-City1"]}">
          <h5><a href="{get_url(line["Q code"])}">{line["Display title"]}</a></h5>
          <p class="ml-2 mb-0">{publication_range}</p>
          <hr/>
          <div class="small px-2 py-1">
          <p>{line["Notes"]}</p>
          <p>{related_items_field}</p>
          </div>
        </div>
      ''')
