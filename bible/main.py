import json

with open("bible\\bibleDict.txt", "r", encoding="utf-8") as f:
    bible = json.load(f)

while True:
    query = str(input("Book Chapter:Verse\n"))
    if query == "":
        break
    try:
        print(bible[query])
    except KeyError:
        print("invalid query")
    print("\n")