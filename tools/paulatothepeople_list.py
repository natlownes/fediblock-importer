# helper script to scrape the PaulaToThePeople list and turn it into a format importable by the importer
# https://joinfediverse.wiki/FediBlock
# usage: python paulatothepeoplelist.py > list.yaml

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import yaml

def _find_table(heading):
  for e in heading.next_siblings:
    if(type(e) == Tag):
      if(e.name == 'table'):
        return e

def main():
  page = requests.get("https://joinfediverse.wiki/FediBlock")
  soup = BeautifulSoup(page.text, "html.parser")

  headings = (
    'Malware &amp; co Blocklist',
    'Worst offenders',
    'Main Blocklist',
  )

  instances = []

  heading_elements = soup.select('h2 .mw-headline')
  list_headings = [h.find_parent('h2') for h in heading_elements if h.decode_contents().strip() in headings]
  for lh in list_headings:
    tbl = _find_table(lh)
    rows = tbl.select('tr')

    for row in rows:
      instance = {}

      host = row.find('th').text.rstrip()
      other = row.find_all('td')

      if host != "instance" and len(host) > 0:
        instance['hostname'] = host
        instance['severity'] = 'suspend'
      else:
        continue

      instances.append(instance)

  print(yaml.dump(instances))

if __name__ == '__main__':
  main()
