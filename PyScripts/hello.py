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




class sayHello:
	# methods
	def add(self, a, b):
		return a + b
	def sub(self, a, b):
		return a - b

# explicit function
def method():
    text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
    return (text)
