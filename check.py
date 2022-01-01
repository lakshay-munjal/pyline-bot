import json

questionaire = {}

with open('./resources/quesaire.json', encoding='utf8') as f:
    questionaire = json.load(f)
    print(questionaire)

print("check")
print(questionaire)