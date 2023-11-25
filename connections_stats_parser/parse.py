from enum import Enum
import re


class Category(Enum):
    YELLOW = '\U0001f7e8'
    GREEN = '\U0001f7e9'
    BLUE = '\U0001f7e6'
    PURPLE = '\U0001f7ea'


connections_pattern = r'Puzzle#(\d+)([🟦🟩🟪🟨]+)'


class Connection:
    def __init__(self, number, order, attempts, won):
        self.number = number
        self.order = order
        self.attempts = attempts
        self.won = won

    def __eq__(self, other):
        return self.number == other.number and \
            self.won == other.won and \
            self.attempts == other.attempts and \
            self.order == other.order


def parse_file(file, seperator):
    attempts = file.read_text().split(seperator)
    return [parse_connection_share(i) for i in attempts]


def parse_connection_share(share):
    # Parses the connection share thingy and returns a Connection object
    num, guesses = parse_connections(share)

    order = []
    for g in guesses:
        guessed = is_correct_guess(g)
        if guessed is not None:
            order.append(guessed)

    won = len(order) == 4

    attempts = len(guesses)

    return Connection(num, order, attempts, won)


def parse_connections(connections):
    # Parse a raw connection attempt and return puzzle_number, array of guesses
    match = re.search(connections_pattern, remove_whitespace(connections))

    if match:
        puzzle_number = match.group(1)
        emojis_group = match.group(2)

        # Convert emojis group to an array
        guesses = []
        for i in range(0, len(emojis_group), 4):
            guesses.append(list(emojis_group[i:i + 4]))

        return int(puzzle_number), guesses


def is_correct_guess(guess):
    # Returns the color of the category guesses. If failed attempt return None
    return guess[0] if guess[0] == guess[1] == guess[2] == guess[3] else None


def remove_whitespace(s):
    # Removes whitespace and newline chars from a string
    return ''.join(s.split())
