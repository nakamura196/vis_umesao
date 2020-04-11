import json

# path to curation
curation_path = "../data/src/curation.json"

count = 0

map = {}

with open(curation_path) as f:
    curation = json.load(f)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            metadata = member["metadata"]

            for obj in metadata:
                label = obj["label"]
                value = obj["value"]

                if label not in map:
                    map[label] = {}

                if value not in map[label]:
                    map[label][value] = []
                
                map[label][value].append(count)

            count += 1


for label in map:

    tmp = {}

    result = []
    items_result = []

    obj = map[label]

    count = 0

    for value in obj:
        result.append({
            "count" : len(obj[value]),
            "index" : count,
            "label" : value,
            "url" : "",
            "value" : value
        })

        for index in obj[value]:
            tmp[index] = count

        count += 1

    for index in sorted(tmp):
        items_result.append(tmp[index])

    OUTPUT_FILE = "../data/"+label+".json"
    with open(OUTPUT_FILE, 'w') as outfile:
        json.dump(result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
    
    OUTPUT_ITEMS_FILE = "../data/item_"+label+".json"
    with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
        json.dump(items_result, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

'''
# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(captureIds, outfile, ensure_ascii=False,
              indent=4, sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(captureIds)) + " lines to " + OUTPUT_FILE)




from collections import Counter
import json
from pprint import pprint
import re
import sys
import urllib

# input
if len(sys.argv) < 3:
    print("Usage: %s <inputfile items json> <outputfile collections json> <outputfile item collections json>" %
          sys.argv[0])
    sys.exit(1)
INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
OUTPUT_ITEMS_FILE = sys.argv[3]

# init
collections = []
item_collections = []


def addCollection(g, url):
    global collections
    global item_collections

    collection = next(
        iter([_g for _g in collections if _g['value'] == g]), False)

    if collection:
        collections[collection['index']]['count'] += 1
    else:
        label = 'Unknown'
        # url = ''
        if g:
            label = g.capitalize()
            # url = 'http://digitalcollections.nypl.org/search/index?utf8=✓&keywords=&filters%5Brights%5D=pd&filters%5Bcollection%5D=' + label
        collection = {
            'index': len(collections),
            'value': g,
            'label': label,
            'url': url,
            'count': 1
        }
        collections.append(collection)

    item_collections.append(collection['index'])


with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

for item in data:

    collection = item["c_label"]
    url = ""
    if "c_url" in item:
        url = item["c_url"]
    addCollection(collection, url)

# Report on collections
collections = sorted(collections, key=lambda d: d['count'], reverse=True)
pprint(collections)

# Write out data
with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(collections, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(collections)) + " collections to " + OUTPUT_FILE)

with open(OUTPUT_ITEMS_FILE, 'w') as outfile:
    json.dump(item_collections, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
print("Wrote " + str(len(item_collections)) + " items to " + OUTPUT_ITEMS_FILE)
'''