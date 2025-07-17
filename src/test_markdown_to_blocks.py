import unittest

from functions import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test the example from the assignment"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        """Test with single block (no blank lines)"""
        md = "This is just a single paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just a single paragraph with no blank lines."])

    def test_markdown_to_blocks_heading_and_paragraph(self):
        """Test with heading and paragraph"""
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            ],
        )

    def test_markdown_to_blocks_multiple_types(self):
        """Test with multiple block types"""
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        """Test with excessive newlines"""
        md = """# Heading


This is a paragraph


- List item 1
- List item 2



Another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph",
                "- List item 1\n- List item 2",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        """Test with leading and trailing whitespace"""
        md = """   # Heading with spaces   

  This is a paragraph with leading and trailing spaces  

   - List item with spaces   
   - Another list item   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "This is a paragraph with leading and trailing spaces",
                "- List item with spaces\n   - Another list item",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        """Test with empty string"""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        """Test with only whitespace"""
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        """Test with only newlines"""
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_code_blocks(self):
        """Test with code blocks"""
        md = """Here's some code:

```python
def hello():
    print("Hello, World!")
```

And here's more text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                "```python\ndef hello():\n    print(\"Hello, World!\")\n```",
                "And here's more text.",
            ],
        )

    def test_markdown_to_blocks_blockquotes(self):
        """Test with blockquotes"""
        md = """# Main heading

> This is a blockquote
> It spans multiple lines
> And continues here

Regular paragraph text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main heading",
                "> This is a blockquote\n> It spans multiple lines\n> And continues here",
                "Regular paragraph text.",
            ],
        )

    def test_markdown_to_blocks_mixed_content(self):
        """Test with mixed content including images and links"""
        md = """# Welcome to My Site

This is a paragraph with a [link](https://example.com) and an ![image](https://example.com/img.png).

## Code Example

Here's some `inline code` and a block:

```
code block here
```

That's all!"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Welcome to My Site",
                "This is a paragraph with a [link](https://example.com) and an ![image](https://example.com/img.png).",
                "## Code Example",
                "Here's some `inline code` and a block:",
                "```\ncode block here\n```",
                "That's all!",
            ],
        )

    def test_markdown_to_blocks_ordered_lists(self):
        """Test with ordered lists"""
        md = """# Tasks

1. First task
2. Second task
3. Third task

Done with tasks."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Tasks",
                "1. First task\n2. Second task\n3. Third task",
                "Done with tasks.",
            ],
        )

    def test_markdown_to_blocks_headers_various_levels(self):
        """Test with various header levels"""
        md = """# H1 Header

## H2 Header

### H3 Header

#### H4 Header

##### H5 Header

###### H6 Header"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# H1 Header",
                "## H2 Header",
                "### H3 Header",
                "#### H4 Header",
                "##### H5 Header",
                "###### H6 Header",
            ],
        )

    def test_markdown_to_blocks_no_final_newline(self):
        """Test with no final newline"""
        md = """First block

Second block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_markdown_to_blocks_single_newline_preservation(self):
        """Test that single newlines within blocks are preserved"""
        md = """# Header

This is line 1
This is line 2
This is line 3

Another block
With multiple lines"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Header",
                "This is line 1\nThis is line 2\nThis is line 3",
                "Another block\nWith multiple lines",
            ],
        )


if __name__ == "__main__":
    unittest.main()
