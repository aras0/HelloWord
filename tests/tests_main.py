import unittest
from helloword import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.tekst = "helo word"

    def test_main(self):
        element = main.main()

        self.assertEqual(element, "helo word")



if __name__ == '__main__':
    unittest.main()
