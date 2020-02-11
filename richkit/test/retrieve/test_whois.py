import unittest

class URLVoidTestCase(unittest.TestCase):
    @unittest.skip("No test has been implemented")
    def test_nothing(self):
        self.fail("No test has been implemented")

if __name__ == '__main__':
    unittest.main()
