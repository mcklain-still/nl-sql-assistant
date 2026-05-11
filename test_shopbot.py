import unittest
from utils import validate_sql, format_results


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


class TestResultFormatting(unittest.TestCase):
    """Test result formatting."""

    def test_empty_results(self):
        result = format_results(["id", "name"], [])
        self.assertEqual(result, "No results found.")

    def test_format_with_data(self):
        columns = ["id", "name"]
        results = [(1, "Product A"), (2, "Product B")]
        result = format_results(columns, results)
        self.assertIn("id | name", result)
        self.assertIn("1 | Product A", result)


if __name__ == "__main__":
    unittest.main()
