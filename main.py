import json
import random


def jsontolist(filename: str) -> list:
    with open(filename) as f:
        words = json.load(f)
    # convert all words to uppercase
    words = [w.upper() for w in words]
    return words


def initialguess(words: list) -> str:
    return random.choice(words)


def getstatus(previousguess: str) -> list:
    currentpos = 0
    greenletters = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: "",
    }
    yellowletters = []
    grayletters = []

    while currentpos < 5:
        status = int(
            input(
                f"What colour is letter {previousguess[currentpos]} of word {previousguess}? \n 1 - Green \n 2 - Yellow \n 3 - Gray \n"
            )
        )
        if status == 1:  # Green
            greenletters[currentpos] = previousguess[currentpos]
            currentpos += 1
        if status == 2:  # Yellow
            yellowletters.append([previousguess[currentpos], currentpos])
            currentpos += 1
        if status == 3:  # Gray
            grayletters.append(previousguess[currentpos])
            currentpos += 1
    return greenletters, yellowletters, grayletters


# Structure
# Greenletter Letter position,letter
# Yellowletter Letter,Position it doesnt work in
# Grayletter letter


def getguess(
    greenletters: dict, yellowletters: list, grayletters: list, wordlist: list
) -> str:
    validwords = []
    for word in wordlist:
        is_valid = True
        for letter in grayletters:
            if letter in word:
                is_valid = False
                break
        if is_valid:
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

    return random.choice(validwords)


if __name__ == "__main__":
    words = jsontolist("validwords.json")
    firstguess = initialguess(words)
    greenletters, yellowletters, grayletters = getstatus(firstguess)
    while "" in greenletters.values():
        guess = getguess(greenletters, yellowletters, grayletters, words)
        greenletters, yellowletters, grayletters = getstatus(guess)

