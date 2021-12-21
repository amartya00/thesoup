import unittest

from thesoup.utilityclasses.result import Result


class TestResult (unittest.TestCase):
    def test_success(self):
        success = Result.success(123)
        self.assertTrue(success)
        self.assertEqual(123, success())

    def test_err(self):
        err = Result.err(123)
        self.assertFalse(err)
        self.assertEqual(123, err())
