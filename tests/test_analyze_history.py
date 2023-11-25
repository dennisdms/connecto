import unittest
from connections_stats_parser import parse, analyze_history
from pathlib import Path


class TestAnalyzeHistory(unittest.TestCase):
    def test_analyze_history(self):
        attempts = get_test_data('test1.txt', '***')
        stats = analyze_history.analyze_history(attempts)
        expected_attempt_matrix = {analyze_history.YELLOW: [2, 0, 2, 1],
                                   analyze_history.GREEN: [1, 2, 0, 2],
                                   analyze_history.BLUE: [2, 2, 1, 0],
                                   analyze_history.PURPLE: [0, 1, 2, 2]}
        self.assertEqual(stats.attempts, 6)
        self.assertEqual(stats.wins, 5)
        self.assertEqual(stats.attempt_distribution, [1, 0, 2, 2])
        self.assertEqual(expected_attempt_matrix, stats.attempt_matrix)


def get_test_data(file, seperator):
    return parse.parse_file(Path('test_data', file), seperator)
