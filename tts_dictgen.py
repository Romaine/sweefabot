"""A reasonable attempt at regex"""
import re

part1 = open("raw_sauce.txt").readlines()
part2 = open("raw_sauce2.txt").readlines()

option = re.compile(".*\((.*?)\).*")
voice = re.compile(".*\[(\d*?)\].*")
lang = re.compile(".*\[(\d*?)\]\[.*")




tts_dict = dict()

for line in part1:
    if line:
        print(line)
        print(option.match(line).group(1))
        tts_dict[eval(option.match(line).group(1))] = []

for line in part2:
    if line:
        print(voice.match(line).group(1),lang.match(line).group(1),option.match(line).group(1))
        for lingo in tts_dict.keys():
            if line[1] == lang.match(line).group(1):
                lingo[1].append((eval(option.match(line).group(1))))

print(tts_dict)
