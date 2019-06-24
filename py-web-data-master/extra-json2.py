import json

data = []

with open('file') as f:
    for line in f:
        data.append(json.loads(line))