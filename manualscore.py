import json
import csv
import pathlib
import random

SCORE_FILE = 'scores.csv'

with open(SCORE_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    scored = {x['hash'] for x in reader}

paths = list(pathlib.Path('.').iterdir())
random.shuffle(paths)

for path in paths:
    if path.suffix != '.json':
        continue
    if path.stem in scored:
        continue
    with path.open() as file_handle:
        json_data = json.load(file_handle)
    for key, value in json_data.items():
        print(key, value)
    score = input('a/b/c/d/f')
    with open(SCORE_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['hash', 'score'])
        writer.writerow({'hash': path.stem, 'score': score})
