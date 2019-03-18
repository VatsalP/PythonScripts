#!/usr/bin/env python3
from sys import argv

def convert(word):
    if word[0] in "aeiouAEIOU":
        pigWord = word + "way"
        return pigWord
    else:
        pigWord = ""
        count = 0
        for ch in word:
            if ch in "aeiouAEIOU":
                pigWord = word[count:] + word[0:count] + "ay"
                return pigWord
            else:
                count += 1

def main():
    try:
        textToConvert = argv[1]
        words = list(textToConvert.split(" "))
        pigified = ""
        for word in words:
            word = convert(word)
            pigified += word + " "
        print(pigified)
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
