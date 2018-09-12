"""A reasonable attempt at regex"""
import json
import re

part1 = open("raw_sauce.txt").readlines()
part2 = open("raw_sauce2.txt").readlines()

option = re.compile(".*n\((.*?)\)(?=;|\s)")
voice = re.compile(".*\[(\d*?/)\].*")
lang = re.compile(".*\[(\d*?)\]\[.*")

tts_dict = dict()

for line in part1:
    if line:
        print(option.match(line).group(1))
        data = eval(option.match(line).group(1))
        tts_dict[data[1]] = [data[0], []]

for line in part2:
    if line:
        for i, lingo in tts_dict.keys():
            if lang.match(line).group(1) == lingo:
                tts_dict[lingo][1].append((option.match(line)
                                                 .group(1))
                                                 .replace("\"", "")
                                                 .split(", "))

print(tts_dict)
with open("tts_dict.json", "w") as out:
    json.dump(tts_dict, out,  ensure_ascii=False, sort_keys=True, indent=4)
