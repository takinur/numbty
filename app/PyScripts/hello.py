import json
import spacy
from spacy import displacy
from rich import print, print_json

x = {
  "name": "John",
  "age": 30,
  "city": "London"
}

# data = json.dumps(x)

# print_json(data)



text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
print(doc)
