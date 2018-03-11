# unit testing

import unittest
import ElvUIMacClient
impoort platform


class TestElvUIMacClient(unittest.TestCase)
    def test_getMacOSVersion(self):
        result = macOSVersion = platform.mac_ver()[0]
        self.assertIsNotNone(result)


if __name__ = '__main__':
    unittest.main()
