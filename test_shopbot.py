import unittest
from utils import validate_sql


class TestSQLValidation(unittest.TestCase):
    """Test SQL validation logic."""

    def test_valid_select(self):
        sql = "SELECT * FROM products WHERE price > 100"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid)

    def test_delete_rejected(self):
        sql = "DELETE FROM products WHERE id = 1"
        is_valid, msg = validate_sql(sql)
        self.assertFalse(is_valid)
        self.assertIn("DELETE", msg)

    def test_drop_rejected(self):
        sql = "DROP TABLE products"
        is_valid, msg = validate_sql(sql)
        self.assertFalse(is_valid)

    def test_non_select_rejected(self):
        sql = "INSERT INTO products VALUES (...)"
        is_valid, msg = validate_sql(sql)
        self.assertFalse(is_valid)

    def test_comment_injection_rejected(self):
        sql = "SELECT * FROM products -- ; DROP TABLE customers"
        is_valid, msg = validate_sql(sql)
        self.assertFalse(is_valid)

    def test_with_cte_accepted(self):
        """Common Table Expressions (WITH) should be accepted as read-only."""
        sql = "WITH ranked AS (SELECT * FROM products) SELECT * FROM ranked"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid)


if __name__ == "__main__":
    unittest.main()