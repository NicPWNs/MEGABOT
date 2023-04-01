import random

# Return random greeting message

def greeting():

    greetings = [
        "Hello there",
        "Hi",
        "Hola",
        "Merhaba",
        "How do you do",
        "Hey",
        "Hello",
        "Yo",
        "Sup",
        "Hey mate",
        "'Ello",
        "Howdy",
        "What's up buttercup",
        "Hey there",
        "G'day",
    ]

    return random.choice(greetings)
