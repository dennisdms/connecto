import unittest
from connections_stats_parser import parse


class TestParse(unittest.TestCase):

    def test_parse_connection_share(self):
        input = """
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
        raw_guesses = [['🟪', '🟩', '🟩', '🟩'],
                       ['🟩', '🟩', '🟪', '🟩'],
                       ['🟦', '🟦', '🟦', '🟦'],
                       ['🟩', '🟩', '🟩', '🟩'],
                       ['🟨', '🟨', '🟪', '🟨'],
                       ['🟨', '🟨', '🟨', '🟨'],
                       ['🟪', '🟪', '🟪', '🟪']]
        attempts = 7
        won = True
        order = ['🟦', '🟩', '🟨', '🟪']
        expected = parse.Connection(puzzle_num, order, attempts, won)
        res = parse.parse_connection_share(input)
        self.assertEquals(res, expected)

    def test_parse_connections(self):
        input = """
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
        res = parse.parse_connections(input)
        self.assertEquals(res, expected)

    def test_is_correct_guess_1(self):
        input = ['🟪', '🟪', '🟪', '🟪']
        expected = '🟪'
        res = parse.is_correct_guess(input)
        self.assertEquals(res, expected)

    def test_is_correct_guess_2(self):
        input = ['🟪', '🟪', '🟪', '🟩']
        res = parse.is_correct_guess(input)
        self.assertIsNone(res)

    def test_remove_special_chars(self):
        input = """
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
        res = parse.remove_whitespace(input)
        self.assertEquals(res, expected)
