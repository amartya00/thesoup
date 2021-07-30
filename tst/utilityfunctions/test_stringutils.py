import unittest

from thesoup.utilityfunctions.stringutils import is_anagram


class TestStringUtils (unittest.TestCase):
    def test_is_anagram(self):
        s1 = "cinema"
        s2 = "iceman"
        s3 = "potato"
        self.assertTrue(is_anagram(s1, s2))
        self.assertFalse(is_anagram(s2, s3))
