"""A reasonable attempt at regex"""
import json
import re

part1 = open("raw_sauce.txt").readlines()
part2 = open("raw_sauce2.txt").readlines()

option = re.compile(".*\((.*?)\)(?=;)")
voice = re.compile(".*\[(\d*?)\].*")
lang = re.compile(".*\[(\d*?)\]\[.*")

tts_dict = dict()

for line in part1:
    if line:
        print(option.match(line).group(1))
        tts_dict[eval(option.match(line).group(1))[1]] = []

for line in part2:
    if line:
        for i, lingo in enumerate(tts_dict.keys()):
            if lang.match(line).group(1) == lingo:#[1]:
                tts_dict[lingo].append((option.match(line).group(1)))

print(tts_dict)
with open("tts_dict.json", "w") as out:
    json.dump(tts_dict, out,  ensure_ascii=False)
