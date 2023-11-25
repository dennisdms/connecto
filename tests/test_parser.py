import unittest
from connections_stats_parser import parse
from pathlib import Path


class TestParse(unittest.TestCase):

    def test_parse_file(self):
        path = Path('test_data', 'test1.txt')
        res = parse.parse_file(path, '***')
        a1 = parse.Connection(166, ['🟦', '🟩', '🟨', '🟪'], 7, True)
        a2 = parse.Connection(166, [], 4, False)
        a3 = parse.Connection(165, ['🟨', '🟦', '🟪', '🟩'], 7, True)
        a4 = parse.Connection(165, ['🟨', '🟦', '🟪', '🟩'], 6, True)
        a5 = parse.Connection(165, ['🟩', '🟪', '🟦', '🟨'], 4, True)
        a6 = parse.Connection(164, ['🟦', '🟩', '🟨', '🟪'], 6, True)
        expected = [a1, a2, a3, a4, a5, a6]
        self.assertEquals(expected, res)

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
        attempts = 7
        won = True
        order = ['🟦', '🟩', '🟨', '🟪']
        expected = parse.Connection(puzzle_num, order, attempts, won)
        res = parse.parse_connection_share(input)
        self.assertEquals(expected, res)

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
        res = parse.guessed_category(input)
        self.assertEquals(expected, res)

    def test_is_correct_guess_2(self):
        input = ['🟪', '🟪', '🟪', '🟩']
        res = parse.guessed_category(input)
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
        self.assertEquals(expected, res)
