import unittest
from functions import block_to_block_type, BlockType

class TestBlockTypes(unittest.TestCase):
    
    def test_heading_blocks(self):
        """Test various heading formats"""
        # Valid headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Invalid headings (no space after #)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##NoSpace"), BlockType.PARAGRAPH)
        
        # Invalid headings (too many #)
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        
        # Invalid headings (# not at start)
        self.assertEqual(block_to_block_type("Not # a heading"), BlockType.PARAGRAPH)
    
    def test_code_blocks(self):
        """Test code block detection"""
        # Valid code blocks
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)  # Empty code block
        
        # Invalid code blocks
        self.assertEqual(block_to_block_type("``code``"), BlockType.PARAGRAPH)  # Only 2 backticks
        self.assertEqual(block_to_block_type("```no closing"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("no opening```"), BlockType.PARAGRAPH)
    
    def test_quote_blocks(self):
        """Test quote block detection"""
        # Valid quotes
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Quote line 1\n>Quote line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Single line quote"), BlockType.QUOTE)
        
        # Invalid quotes (not all lines start with >)
        self.assertEqual(block_to_block_type(">Quote line 1\nNot a quote"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a quote\n>Quote line 2"), BlockType.PARAGRAPH)
    
    def test_unordered_list_blocks(self):
        """Test unordered list detection"""
        # Valid unordered lists
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
        
        # Invalid unordered lists (missing space after -)
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item 1\n-NoSpace"), BlockType.PARAGRAPH)
        
        # Invalid unordered lists (not all lines start with -)
        self.assertEqual(block_to_block_type("- Item 1\nNot a list item"), BlockType.PARAGRAPH)
    
    def test_ordered_list_blocks(self):
        """Test ordered list detection"""
        # Valid ordered lists
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)
        
        # Invalid ordered lists (wrong numbering)
        self.assertEqual(block_to_block_type("2. Item 1"), BlockType.PARAGRAPH)  # Doesn't start with 1
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2"), BlockType.PARAGRAPH)  # Skips 2
        self.assertEqual(block_to_block_type("1. Item 1\n1. Item 2"), BlockType.PARAGRAPH)  # Doesn't increment
        
        # Invalid ordered lists (wrong format)
        self.assertEqual(block_to_block_type("1.NoSpace"), BlockType.PARAGRAPH)  # No space after .
        self.assertEqual(block_to_block_type("1) Item 1"), BlockType.PARAGRAPH)  # Wrong punctuation
        
        # Invalid ordered lists (not all lines are list items)
        self.assertEqual(block_to_block_type("1. Item 1\nNot a list item"), BlockType.PARAGRAPH)
    
    def test_paragraph_blocks(self):
        """Test paragraph detection (default case)"""
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("This is a paragraph\nwith multiple lines."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Text with **bold** and _italic_."), BlockType.PARAGRAPH)
    
    def test_edge_cases(self):
        """Test edge cases and complex examples"""
        # Empty lines in quotes (should still be quote if non-empty lines start with >)
        self.assertEqual(block_to_block_type(">Quote\n\n>More quote"), BlockType.QUOTE)
        
        # Mixed content that should be paragraph
        self.assertEqual(block_to_block_type("#Not a heading because no space\n- Not a list"), BlockType.PARAGRAPH)
        
        # Complex code block
        code_block = "```python\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        
        # Long ordered list
        long_list = "\n".join([f"{i}. Item {i}" for i in range(1, 6)])
        self.assertEqual(block_to_block_type(long_list), BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
