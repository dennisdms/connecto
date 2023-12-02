import re
from pathlib import Path


# Connections consists of four groups where each group is a category
class ConnectionsResult:
    # A single connections result
    def __init__(
        self, puzzle_number: int, group_order: list[str], mistakes: int, won: int
    ) -> None:
        self.puzzle_number = puzzle_number
        self.group_order = group_order
        self.mistakes = mistakes
        self.won = won

    def __eq__(self, other) -> bool:
        return (
            self.puzzle_number == other.puzzle_number
            and self.won == other.won
            and self.mistakes == other.mistakes
            and self.group_order == other.group_order
        )


class ConnectionsStats:
    # Aggregated statistics for a series of ConnectionsResults
    def __init__(
        self,
        attempts: int,
        wins: int,
        mistake_distribution: list[int],
        attempt_matrix: dict[str, list[int]],
    ):
        self.attempts = attempts
        self.wins = wins
        self.mistake_distribution = mistake_distribution
        self.attempt_matrix = attempt_matrix

    def display(self) -> str:
        if self.attempts == 0:
            return "No games played"

        return f"Plays: {self.attempts}, Wins: {self.wins} ({round(self.wins / self.attempts * 100, 2)} %)\n\nMistakes\n{self.display_stats_pretty()}\n\nGrouping Order\n{self.grouping_order_stats_pretty()}"

    def display_stats_pretty(self) -> str:
        out = [
            f"{i} Mistake(s): {self.mistake_distribution[i]}"
            for i in range(len(self.mistake_distribution))
        ]
        return "\n".join(out)

    def grouping_order_stats_pretty(self) -> str:
        out = "   1 2 3 4\n"
        for group, attempts in self.attempt_matrix.items():
            a_str = ""
            for a in attempts:
                a_str = a_str + str(a) + " "
            out = out + f"{group} {a_str}\n"

        return out

    def __eq__(self, other) -> bool:
        return (
            self.attempts == other.attempts
            and self.wins == other.wins
            and self.mistake_distribution == other.mistake_distribution
            and self.attempt_matrix == other.attempt_matrix
        )


YELLOW = "\U0001f7e8"
GREEN = "\U0001f7e9"
BLUE = "\U0001f7e6"
PURPLE = "\U0001f7ea"


def analyze_connections_history(
    connections_attempts: list[ConnectionsResult],
) -> ConnectionsStats:
    wins = 0
    mistake_distribution = [0, 0, 0, 0, 0]
    attempt_matrix = {
        YELLOW: [0, 0, 0, 0],
        GREEN: [0, 0, 0, 0],
        BLUE: [0, 0, 0, 0],
        PURPLE: [0, 0, 0, 0],
    }
    for attempt in connections_attempts:
        assert 0 <= attempt.mistakes <= 4
        mistake_distribution[attempt.mistakes] += 1
        if attempt.won:
            wins += 1
            for i, category in enumerate(attempt.group_order):
                attempt_matrix.get(category)[i] += 1

    return ConnectionsStats(
        len(connections_attempts), wins, mistake_distribution, attempt_matrix
    )


def parse_connections_result(result: str) -> ConnectionsResult:
    # Parses a connections result into a ConnectionsResult object. Returns None if it can't be parsed
    out = parse_connections_share_string(result)
    mistakes = 0
    if out is not None:
        num, guesses = out
        order = []
        for g in guesses:
            guessed = grouped_category(g)
            if guessed is not None:
                order.append(guessed)
            else:
                mistakes += 1
        won = len(order) == 4
        return ConnectionsResult(num, order, mistakes, won)


connections_pattern = r"ConnectionsPuzzle#(\d+)([🟦🟩🟪🟨]+)"


def parse_connections_share_string(connections: str) -> tuple[int, list[list[str]]]:
    # Parse a raw connection attempt and return puzzle_number, array of guesses
    match = re.search(connections_pattern, remove_whitespace(connections))
    if match:
        puzzle_number = match.group(1)
        emojis_group = match.group(2)
        guesses = []
        for i in range(0, len(emojis_group), 4):
            guesses.append(list(emojis_group[i : i + 4]))

        return int(puzzle_number), guesses


def grouped_category(guess: list[str]) -> str:
    # Returns the category correctly grouped. If failed, return None
    return guess[0] if guess[0] == guess[1] == guess[2] == guess[3] else None


def parse_file(file: Path, seperator: str) -> list[ConnectionsResult]:
    # Parses a file of connections results - used primarily for testing
    attempts = file.read_text(encoding="utf-8").split(seperator)
    results = []
    for attempt in attempts:
        parsed_attempt = parse_connections_result(attempt)
        if parsed_attempt is not None:
            results.append(parsed_attempt)
    return results


def is_parsable(possible_connections_game: str) -> bool:
    return bool(re.fullmatch(connections_pattern, possible_connections_game))


def remove_whitespace(s: str) -> str:
    """Removes whitespace and newline chars from a string"""
    return "".join(s.split())


def parse_messages(messages: list[str]) -> ConnectionsStats:
    """Parses the given messages into connections stats."""
    games = {}
    for message in messages:
        res = parse_connections_result(message)
        if res is not None:
            games[res.puzzle_number] = res

    return analyze_connections_history(list(games.values()))
