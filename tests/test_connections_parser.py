import unittest
from connecto import connections_parser
from pathlib import Path


class TestConnectionsParser(unittest.TestCase):

    def test_stats_display(self):
        result = parse_test_file('test1.txt', '***')
        stats = connections_parser.analyze_connections_history(result)
        print(stats.display())

    def test_analyze_history(self):
        attempts = parse_test_file('test1.txt', '***')
        stats = connections_parser.analyze_connections_history(attempts)
        expected_attempt_matrix = {connections_parser.YELLOW: [2, 0, 2, 1],
                                   connections_parser.GREEN: [1, 2, 0, 2],
                                   connections_parser.BLUE: [2, 2, 1, 0],
                                   connections_parser.PURPLE: [0, 1, 2, 2]}
        self.assertEqual(stats.attempts, 6)
        self.assertEqual(stats.wins, 5)
        self.assertEqual(stats.attempt_distribution, [1, 0, 2, 2])
        self.assertEqual(expected_attempt_matrix, stats.attempt_matrix)

    def test_parse_file(self):
        res = parse_test_file('test1.txt', '***')
        a1 = connections_parser.ConnectionsResult(166, ['🟦', '🟩', '🟨', '🟪'], 7, True)
        a2 = connections_parser.ConnectionsResult(166, [], 4, False)
        a3 = connections_parser.ConnectionsResult(165, ['🟨', '🟦', '🟪', '🟩'], 7, True)
        a4 = connections_parser.ConnectionsResult(165, ['🟨', '🟦', '🟪', '🟩'], 6, True)
        a5 = connections_parser.ConnectionsResult(165, ['🟩', '🟪', '🟦', '🟨'], 4, True)
        a6 = connections_parser.ConnectionsResult(164, ['🟦', '🟩', '🟨', '🟪'], 6, True)
        expected = [a1, a2, a3, a4, a5, a6]
        self.assertEquals(expected, res)

    def test_parse_file_empty(self):
        res = parse_test_file('empty.txt', '***')
        self.assertEquals(0, len(res))

    def test_parse_connection_share(self):
        player_input = """
        Connections
        Puzzle #166
        🟪🟩🟩🟩
        🟩🟩🟪🟩
        🟦🟦🟦🟦
        🟩🟩🟩🟩
        🟨🟨🟪🟨
        🟨🟨🟨🟨
        🟪🟪🟪🟪
        """
        puzzle_num = 166
        attempts = 7
        won = True
        order = ['🟦', '🟩', '🟨', '🟪']
        expected = connections_parser.ConnectionsResult(puzzle_num, order, attempts, won)
        res = connections_parser.parse_connections_result(player_input)
        self.assertEquals(expected, res)

    def test_parse_connections(self):
        player_input = """
        Connections
        Puzzle #166
        🟪🟩🟩🟩
        🟩🟩🟪🟩
        🟦🟦🟦🟦
        🟩🟩🟩🟩
        🟨🟨🟪🟨
        🟨🟨🟨🟨
        🟪🟪🟪🟪
        """
        expected = (166, [['🟪', '🟩', '🟩', '🟩'],
                          ['🟩', '🟩', '🟪', '🟩'],
                          ['🟦', '🟦', '🟦', '🟦'],
                          ['🟩', '🟩', '🟩', '🟩'],
                          ['🟨', '🟨', '🟪', '🟨'],
                          ['🟨', '🟨', '🟨', '🟨'],
                          ['🟪', '🟪', '🟪', '🟪']])
        res = connections_parser.parse_connections_share_string(player_input)
        self.assertEquals(res, expected)

    def test_is_correct_guess_1(self):
        guess = ['🟪', '🟪', '🟪', '🟪']
        expected = '🟪'
        res = connections_parser.grouped_category(guess)
        self.assertEquals(expected, res)

    def test_is_correct_guess_2(self):
        guess = ['🟪', '🟪', '🟪', '🟩']
        res = connections_parser.grouped_category(guess)
        self.assertIsNone(res)

    def test_remove_whitespace(self):
        player_input = """
        Connections
        Puzzle #166
        🟪🟩🟩🟩
        🟩🟩🟪🟩
        🟦🟦🟦🟦
        🟩🟩🟩🟩
        🟨🟨🟪🟨
        🟨🟨🟨🟨
        🟪🟪🟪🟪
        """
        expected = """ConnectionsPuzzle#166🟪🟩🟩🟩🟩🟩🟪🟩🟦🟦🟦🟦🟩🟩🟩🟩🟨🟨🟪🟨🟨🟨🟨🟨🟪🟪🟪🟪"""
        res = connections_parser.remove_whitespace(player_input)
        self.assertEquals(expected, res)


def parse_test_file(file, seperator):
    return connections_parser.parse_file(Path('test_data', file), seperator)
