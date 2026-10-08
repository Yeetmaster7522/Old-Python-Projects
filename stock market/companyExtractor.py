from csv import DictReader
from json import dump

data = []

with open("Python stuff/neural networks/stock market/ASX_Listed_Companies_05-01-2026_02-15-35_AEDT.csv", mode="r", encoding="utf-8", newline="") as f:
    reader = DictReader(f)
    for row in reader:
        data.append(row["ASX code"])

with open("Python stuff/neural networks/stock market/asxCodes.json", "w") as f:
    dump(data, f, indent=4)