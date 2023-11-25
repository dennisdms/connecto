from enum import Enum
import re
from pathlib import Path


# TODO be able to parse a file where \r\n or \n is the seperator between attempts
# TODO create ASCII Histogram for showing the attempt distribution and all the stats in general
# TODO Connect to a discord channel
# TODO create a dockerfile to run this and pass the API token and bot name as config
# TODO run image on dwlabs server and connect it to squinner

# Connections consists of four groups where each group is a category
class ConnectionsResult:
    # A single connections result
    def __init__(self, puzzle_number: int, group_order: list[str], attempts: int, won: int) -> None:
        self.puzzle_number = puzzle_number
        self.group_order = group_order
        self.attempts = attempts
        self.won = won

    def __eq__(self, other) -> bool:
        return self.puzzle_number == other.puzzle_number and \
            self.won == other.won and \
            self.attempts == other.attempts and \
            self.group_order == other.group_order


class ConnectionsStats:
    # Aggregated statistics for a series of ConnectionsResults
    def __init__(self, attempts: int, wins: int, attempt_distribution: list[int], attempt_matrix: dict[str, list[int]]):
        self.attempts = attempts
        self.wins = wins
        self.attempt_distribution = attempt_distribution
        self.attempt_matrix = attempt_matrix


YELLOW = '\U0001f7e8'
GREEN = '\U0001f7e9'
BLUE = '\U0001f7e6'
PURPLE = '\U0001f7ea'


def analyze_connections_history(connections_attempts: list[ConnectionsResult]) -> ConnectionsStats:
    wins = 0
    attempt_distribution = [0, 0, 0, 0]
    attempt_matrix = {YELLOW: [0, 0, 0, 0],
                      GREEN: [0, 0, 0, 0],
                      BLUE: [0, 0, 0, 0],
                      PURPLE: [0, 0, 0, 0]}
    for attempt in connections_attempts:
        if attempt.won:
            wins += 1
            attempt_distribution[attempt.attempts - 4] += 1
            for i, category in enumerate(attempt.group_order):
                attempt_matrix.get(category)[i] += 1

    return ConnectionsStats(len(connections_attempts), wins, attempt_distribution, attempt_matrix)


def parse_connections_result(result: str) -> ConnectionsResult:
    # Parses a connections result into a ConnectionsResult object
    num, guesses = parse_connections_share_string(result)
    order = []
    for g in guesses:
        guessed = grouped_category(g)
        if guessed is not None:
            order.append(guessed)
    attempts = len(guesses)
    won = len(order) == 4
    return ConnectionsResult(num, order, attempts, won)


connections_pattern = r'Puzzle#(\d+)([🟦🟩🟪🟨]+)'


def parse_connections_share_string(connections: str) -> tuple[int, list[list[str]]]:
    # Parse a raw connection attempt and return puzzle_number, array of guesses
    match = re.search(connections_pattern, remove_whitespace(connections))
    if match:
        puzzle_number = match.group(1)
        emojis_group = match.group(2)
        guesses = []
        for i in range(0, len(emojis_group), 4):
            guesses.append(list(emojis_group[i:i + 4]))

        return int(puzzle_number), guesses


def grouped_category(guess: list[str]) -> str:
    # Returns the category correctly grouped. If failed, return None
    return guess[0] if guess[0] == guess[1] == guess[2] == guess[3] else None


def parse_file(file: Path, seperator: str) -> list[ConnectionsResult]:
    # Parses a file of connections results - used primarily for testing
    attempts = file.read_text().split(seperator)
    return [parse_connections_result(i) for i in attempts]


def remove_whitespace(s: str) -> str:
    # Removes whitespace and newline chars from a string
    return ''.join(s.split())
