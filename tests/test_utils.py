import os
import unittest
from datetime import datetime

from replit import db

from utils import daily_update_url, generate_random_string, get_current_url


class TestUtils(unittest.TestCase):
    def test_generate_random_string(self):
        s = generate_random_string(8)
        self.assertEqual(len(s), 8)
        self.assertTrue(all(c.islower() or c.isdigit() for c in s))

    def test_daily_update_url(self):
        if os.getenv("REPLIT_DEPLOYMENT") == "1":
            self.assertIn(os.environ["TEACHER_URL"], daily_update_url())

    def test_get_current_url(self):
        if os.getenv("REPLIT_DEPLOYMENT") == "1":
            demo_url = get_current_url(is_demo=True)
            self.assertEqual(demo_url, f"{os.environ['TEACHER_URL']}")
            real_url = get_current_url(is_demo=False)
            self.assertNotEqual(
                real_url,
                f"{os.environ['TEACHER_URL']}?url_suffix={db.get('url_suffix', '')}",
            )


if __name__ == "__main__":
    unittest.main()
