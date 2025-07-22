import unittest
from functions import extract_title


class TestExtractTitle(unittest.TestCase):
    
    def test_extract_simple_title(self):
        """Test extracting a simple h1 title."""
        markdown = "# Hello"
        expected = "Hello"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_extract_title_with_whitespace(self):
        """Test extracting title with leading/trailing whitespace."""
        markdown = "#   Hello World   "
        expected = "Hello World"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_extract_title_multiline(self):
        """Test extracting title from multiline markdown."""
        markdown = """Some text before

# Main Title

Some content after"""
        expected = "Main Title"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_extract_title_with_content(self):
        """Test extracting title when there's other content."""
        markdown = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**."""
        expected = "Tolkien Fan Club"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_ignores_h2_and_higher(self):
        """Test that only h1 is extracted, not h2, h3, etc."""
        markdown = """## This is h2

### This is h3

# This is h1

#### This is h4"""
        expected = "This is h1"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_first_h1_wins(self):
        """Test that the first h1 is returned when multiple exist."""
        markdown = """# First Title

Some content

# Second Title"""
        expected = "First Title"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)
    
    def test_no_h1_raises_exception(self):
        """Test that missing h1 raises ValueError."""
        markdown = """## Only h2 here

### And h3

Some paragraph text."""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_empty_markdown_raises_exception(self):
        """Test that empty markdown raises ValueError."""
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_only_hashtag_no_title_raises_exception(self):
        """Test that lone # without title raises ValueError."""
        markdown = "# "
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_hashtag_with_complex_title(self):
        """Test title with special characters and formatting."""
        markdown = "# The Lord of the Rings: A Journey Through Middle-earth (Part 1)"
        expected = "The Lord of the Rings: A Journey Through Middle-earth (Part 1)"
        actual = extract_title(markdown)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
