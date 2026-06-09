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

    def test_comment_in_string_literal_accepted(self):
        """SQL with -- inside a string literal should not be rejected as comment injection."""
        sql = "SELECT * FROM products WHERE name LIKE '%something -- cool%'"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid, msg)

    def test_block_comment_injection_rejected(self):
        """Block comment /* */ should be rejected (either via comment or forbidden keyword check)."""
        sql = "SELECT * FROM products /* ; DROP TABLE customers */"
        is_valid, msg = validate_sql(sql)
        self.assertFalse(is_valid)

    def test_show_accepted(self):
        """SHOW statements should be accepted as read-only."""
        sql = "SHOW TABLES"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid, msg)

    def test_describe_accepted(self):
        """DESCRIBE statements should be accepted as read-only."""
        sql = "DESCRIBE products"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid, msg)

    def test_explain_accepted(self):
        """EXPLAIN statements should be accepted as read-only."""
        sql = "EXPLAIN SELECT * FROM products"
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid, msg)

    def test_comment_in_double_quoted_string_accepted(self):
        """SQL with -- inside a double-quoted string should not be rejected."""
        sql = 'SELECT * FROM products WHERE name = "something -- cool"'
        is_valid, msg = validate_sql(sql)
        self.assertTrue(is_valid, msg)


if __name__ == "__main__":
    unittest.main()
