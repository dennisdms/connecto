# Want to show:
# 1. Total number of games played
# 2. Number of games won
# 3. Average number of tries (4 - 7) (attempt distribution)
# 4. Guess matrix
# 4.1 How many times have you guessed purple first?

# TODO switch actual and expected
# TODO Move this stuff into parse
# TODO figure out better naming for all this stuff
# TODO be able to parse a file where \r\n or \n is the seperator between attempts
# TODO create ASCII Histogram for showing the attempt distribution and all the stats in general
# TODO Connect to a discord channel
# TODO create a dockerfile to run this and pass the API token and bot name as config
# TODO run image on dwlabs server and connect it to squinner

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
