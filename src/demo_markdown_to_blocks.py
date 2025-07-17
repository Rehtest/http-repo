#!/usr/bin/env python3
"""
Demo script for markdown_to_blocks function.
Shows how to split markdown text into block-level sections.
"""

from functions import markdown_to_blocks

# Test markdown text with various block types
markdown_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

```
This is a code block
```

> This is a quote
> block

## Another heading

And a final paragraph."""

print("Original markdown text:")
print(repr(markdown_text))
print("\n" + "="*50 + "\n")

# Split into blocks
blocks = markdown_to_blocks(markdown_text)

print(f"Split into {len(blocks)} blocks:")
for i, block in enumerate(blocks, 1):
    print(f"\nBlock {i}:")
    print(f"  Type: {type(block)}")
    print(f"  Content: {repr(block)}")
    print(f"  Display:")
    print(f"    {block}")

# Test with whitespace issues
print("\n" + "="*50 + "\n")
print("Test with whitespace issues:")

whitespace_markdown = """   # Heading with spaces   

   This is a paragraph with spaces   



Another paragraph after multiple blank lines   """

print("Original with whitespace:")
print(repr(whitespace_markdown))

cleaned_blocks = markdown_to_blocks(whitespace_markdown)
print(f"\nCleaned into {len(cleaned_blocks)} blocks:")
for i, block in enumerate(cleaned_blocks, 1):
    print(f"Block {i}: {repr(block)}")

# Test edge cases
print("\n" + "="*50 + "\n")
print("Edge cases:")

# Empty string
empty_result = markdown_to_blocks("")
print(f"Empty string: {empty_result}")

# Only whitespace
whitespace_result = markdown_to_blocks("   \n\n   ")
print(f"Only whitespace: {whitespace_result}")

# Single block
single_result = markdown_to_blocks("Just one block with no blank lines")
print(f"Single block: {single_result}")
