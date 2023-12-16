import unittest
import io
from wssgui.main_window import ResultsParse

class TestResultsParse(unittest.TestCase):
    def test_parse_it(self):
        rp = ResultsParse(
            io.StringIO(
                "xxx\n3\n\tabc\n\tdef\n4\n\tghij\n\tklmn\n"))
        rp.parse_it()
        self.assertEqual(rp.words,
                         {3: ["abc", "def"],
                          4: ["ghij", "klmn"]})

if __name__ == "__main__":
    unittest.main()
