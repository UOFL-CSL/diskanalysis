# Fio Data Parser
import json
import matplotlib as plt

output = open("results.txt")

parsed = json.load(output)

print(parsed["jobs"][0]["write"]["runtime"])