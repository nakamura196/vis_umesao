from collections import Counter
import json
import math
from pprint import pprint
import re
import sys
import urllib.request
import glob

files = glob.glob(
    "/Users/nakamura/git/d_umesao/umesao_images/docs/iiif/item/*/manifest.json")
files = sorted(files)

selections = []

prefix = "https://nakamura196.github.io/vis_umesao"

for i in range(len(files)):
    file = files[i]

    # メイン
    if i % 1000 == 0:
        print(str(i+1)+"/"+str(len(files))+"\t"+file)

    with open(file) as f:
        manifest = json.load(f)

        manifest_uri = manifest["@id"]

        id = manifest_uri.split("/")[-2]

        metadata = []

        if "metadata" in manifest:

            metadata_old = manifest["metadata"]

            for obj in metadata_old:
                if obj["label"] == "資料種別":
                    metadata.append(obj)

        canvases = manifest["sequences"][0]["canvases"]
        if len(canvases) == 0:
            continue

        member = {
            "@id": canvases[0]["@id"],
            "id" : id,
            "@type": "sc:Canvas",
            "label": manifest["label"],
            "metadata": metadata,
            "thumbnail": manifest["thumbnail"]["@id"],
            "related": "https://umesao.cultural.jp/item/"+id
        }

        members = [member]

        selection = {
            "@id": prefix + "/iiif/curation/"+id+"/range1",
            "@type": "sc:Range",
            "label": "Characters",
            "members": members,
            "within": {
                "@id": manifest_uri,
                "@type": "sc:Manifest",
                "label": manifest["label"]
            }
        }
        selections.append(selection)


OUTPUT_FILE = "../data/src/curation.json"


curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": prefix + "/iiif/curation/curation.json",
    "@type": "cr:Curation",
    "label": "Character List",
    "selections": selections
}

fw = open(OUTPUT_FILE, 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
