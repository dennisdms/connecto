from enum import Enum
import re


# TODO Move this stuff into parse
# TODO figure out better naming for all this stuff
# TODO be able to parse a file where \r\n or \n is the seperator between attempts
# TODO create ASCII Histogram for showing the attempt distribution and all the stats in general
# TODO Connect to a discord channel
# TODO create a dockerfile to run this and pass the API token and bot name as config
# TODO run image on dwlabs server and connect it to squinner

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


class ConnectionsStats:
    def __init__(self, attempts, wins, attempt_distribution, attempt_matrix):
        self.attempts = attempts
        self.wins = wins
        self.attempt_distribution = attempt_distribution
        self.attempt_matrix = attempt_matrix


YELLOW = '\U0001f7e8'
GREEN = '\U0001f7e9'
BLUE = '\U0001f7e6'
PURPLE = '\U0001f7ea'


def analyze_history(connections_attempts):
    wins = 0
    attempt_distribution = [0, 0, 0, 0]
    attempt_matrix = {YELLOW: [0, 0, 0, 0], GREEN: [0, 0, 0, 0], BLUE: [0, 0, 0, 0], PURPLE: [0, 0, 0, 0]}
    for attempt in connections_attempts:
        if attempt.won:
            wins += 1
            attempt_distribution[attempt.attempts - 4] += 1
            for i, category in enumerate(attempt.order):
                attempt_matrix.get(category)[i] += 1

    stats = ConnectionsStats(len(connections_attempts), wins, attempt_distribution, attempt_matrix)
    return stats


def parse_connection_share(share):
    # Parses the connection share thingy and returns a Connection object
    num, guesses = parse_connections(share)
    order = []
    for g in guesses:
        guessed = guessed_category(g)
        if guessed is not None:
            order.append(guessed)
    attempts = len(guesses)
    won = len(order) == 4
    return Connection(num, order, attempts, won)


connections_pattern = r'Puzzle#(\d+)([🟦🟩🟪🟨]+)'


def parse_connections(connections):
    # Parse a raw connection attempt and return puzzle_number, array of guesses
    match = re.search(connections_pattern, remove_whitespace(connections))
    if match:
        puzzle_number = match.group(1)
        emojis_group = match.group(2)
        guesses = []
        for i in range(0, len(emojis_group), 4):
            guesses.append(list(emojis_group[i:i + 4]))

        return int(puzzle_number), guesses


def guessed_category(guess):
    # Returns the color of the category guesses. If failed return None
    return guess[0] if guess[0] == guess[1] == guess[2] == guess[3] else None


def parse_file(file, seperator):
    # Parses a file of connections attempts - used primarily for testing
    attempts = file.read_text().split(seperator)
    return [parse_connection_share(i) for i in attempts]


def remove_whitespace(s):
    # Removes whitespace and newline chars from a string
    return ''.join(s.split())
