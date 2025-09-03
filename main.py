import json
import random


def jsontolist(filename: str):
    with open(filename) as f:
        words = json.load(f)
    # convert all words to uppercase
    words = [w.upper() for w in words]
    return words


def initialguess(words: list):
    return words[random.randint(0, (len(words) - 1))]


def getgreen():
    greenletters = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: "",
    }
    currentpos = 0
    while currentpos < 5:
        letter = str(
            input(f"Green Letter at position {currentpos + 1}, or empty if none: ")
        )
        if letter == "":
            currentpos += 1
        if letter.isalpha() and len(letter) == 1:
            greenletters[currentpos] = letter.upper()
            currentpos += 1
    return greenletters


def getyellow(greenletters: dict):
    yellowletters = []
    currentpos = 0
    while currentpos < 5:
        if greenletters[currentpos] != "":
            currentpos += 1
        letter = str(
            input(f"Yellow Letter at position {currentpos + 1}, or empty if none: ")
        )
        if letter == "":
            currentpos += 1
        if letter.isalpha() and len(letter) == 1:
            yellowletters.append([letter.upper(), currentpos])
            currentpos += 1
    return yellowletters


def getgray(greenletters: dict):
    grayletters = []
    for pos in range(5):
        if greenletters[pos] == "":
            letter = str(
                input(f"Gray Letter at position {pos + 1}, or empty if yellow: ")
            )
            if letter.isalpha() and len(letter) == 1:
                grayletters.append(letter.upper())
    return grayletters


def getvalidwords(
    greenletters: dict, yellowletters: list, grayletters: list, words: list
):
    validwords = []
    for word in words:
        is_valid = True
        for letter in grayletters:
            if letter in word:
                is_valid = False
                break
        for pos, letter in greenletters.items():
            if letter != "" and word[pos] != letter:
                is_valid = False
                break
        if is_valid:
            for letter, bad_pos in yellowletters:
                if letter not in word or word[bad_pos] == letter:
                    is_valid = False
                    break
        if is_valid:
            validwords.append(word)
    return validwords


def main(wordfile):
    wordlist = jsontolist(wordfile)
    firstguess = initialguess(wordlist)
    yellowletters = []
    found = False
    print(f"Try {firstguess}")
    while not found:
        greenletters = getgreen()
        grayletters = getgray(greenletters)
        yellowletters.extend(getyellow(greenletters))
        possiblewords = getvalidwords(
            greenletters, yellowletters, grayletters, wordlist
        )
        print(f"Try {possiblewords[0]}")
        if len(possiblewords) == 1:
            found = True


if __name__ == "__main__":
    main("validwords.json")
