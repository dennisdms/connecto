import unittest
from connections_stats_parser import parse
from pathlib import Path


class TestParse(unittest.TestCase):

    def test_analyze_history(self):
        attempts = parse_test_file('test1.txt', '***')
        stats = parse.analyze_history(attempts)
        expected_attempt_matrix = {parse.YELLOW: [2, 0, 2, 1],
                                   parse.GREEN: [1, 2, 0, 2],
                                   parse.BLUE: [2, 2, 1, 0],
                                   parse.PURPLE: [0, 1, 2, 2]}
        self.assertEqual(stats.attempts, 6)
        self.assertEqual(stats.wins, 5)
        self.assertEqual(stats.attempt_distribution, [1, 0, 2, 2])
        self.assertEqual(expected_attempt_matrix, stats.attempt_matrix)

    def test_parse_file(self):
        res = parse_test_file('test1.txt', '***')
        a1 = parse.Connection(166, ['🟦', '🟩', '🟨', '🟪'], 7, True)
        a2 = parse.Connection(166, [], 4, False)
        a3 = parse.Connection(165, ['🟨', '🟦', '🟪', '🟩'], 7, True)
        a4 = parse.Connection(165, ['🟨', '🟦', '🟪', '🟩'], 6, True)
        a5 = parse.Connection(165, ['🟩', '🟪', '🟦', '🟨'], 4, True)
        a6 = parse.Connection(164, ['🟦', '🟩', '🟨', '🟪'], 6, True)
        expected = [a1, a2, a3, a4, a5, a6]
        self.assertEquals(expected, res)

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
        expected = parse.Connection(puzzle_num, order, attempts, won)
        res = parse.parse_connection_share(player_input)
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
        res = parse.parse_connections(player_input)
        self.assertEquals(res, expected)

    def test_is_correct_guess_1(self):
        guess = ['🟪', '🟪', '🟪', '🟪']
        expected = '🟪'
        res = parse.guessed_category(guess)
        self.assertEquals(expected, res)

    def test_is_correct_guess_2(self):
        guess = ['🟪', '🟪', '🟪', '🟩']
        res = parse.guessed_category(guess)
        self.assertIsNone(res)

    def test_remove_special_chars(self):
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
        res = parse.remove_whitespace(player_input)
        self.assertEquals(expected, res)


def parse_test_file(file, seperator):
    return parse.parse_file(Path('test_data', file), seperator)
