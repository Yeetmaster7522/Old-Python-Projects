import json

bible = {}

with open("bible\\bible.txt", "r", encoding="utf-8") as f:
    print("loading raw bible text")
    for line in f:
        entry = line.split("\t")
        bible[entry[0].lower()] = entry[1].strip()
    print("loaded raw bible text")

with open("bible\\bibleDict.txt", "w", encoding="utf-8") as f:
    json.dump(bible, f)
    print("new bible dict created")