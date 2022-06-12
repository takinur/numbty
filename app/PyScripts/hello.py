import json
# from rich import print, print_json
#Find the even numbers in a list
# for i in range(1,11):
#     if i%2==0:
#         print(i)
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
print(json.dumps(x))

