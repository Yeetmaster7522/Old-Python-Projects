import json

def read_first_5(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Print the first 5 items
    for entry in data[:5]:
        print(entry)

    return data[:5]

read_first_5("Python stuff/neural networks/language/data.txt")