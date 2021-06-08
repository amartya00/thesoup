import unittest

from thesoup.utilityclasses.trie import Trie


class TestTrie (unittest.TestCase):
    def test_insert_and_search(self):
        test_trie = Trie()
        test_trie.insert("abcd")
        test_trie.insert("abcde")
        test_trie.insert("axyz")

        self.assertTrue("abcd" in test_trie)
        self.assertTrue("abcde" in test_trie)
        self.assertTrue("axyz" in test_trie)
        self.assertFalse("abc" in test_trie)
        self.assertFalse("pop" in test_trie)

    def test_index(self):
        test_trie = Trie()
        test_trie.insert("abcd")
        test_trie.insert("abcde")
        test_trie.insert("axyz")

        self.assertEqual(["abcde", "abcd", "abde"].sort(), test_trie["ab"].sort())
        self.assertEqual(["abcde", "abcd", "abde"].sort(), test_trie["abcd"].sort())
        self.assertEqual(["abcde", "abcd", "abde", "axyz"].sort(), test_trie["a"].sort())
        self.assertEqual(["axyz"].sort(), test_trie["ax"].sort())
        self.assertEqual(["axyz"].sort(), test_trie["axyz"].sort())
