#!/usr/bin/env python3
"""
Demo script for block_to_block_type function.
Shows how to detect different types of markdown blocks.
"""

from functions import block_to_block_type, BlockType, markdown_to_blocks

def main():
    """Demonstrate block type detection on various markdown examples."""
    
    # Sample markdown document
    markdown_doc = """# Main Heading

This is a normal paragraph with some **bold** text and _italic_ text.

## Subheading

Here's another paragraph that spans
multiple lines but is still one block.

```python
def hello_world():
    print("Hello, World!")
    return True
```

> This is a quote block.
> It can span multiple lines.
> Each line starts with >.

- This is an unordered list
- With multiple items
- Each starting with -

1. This is an ordered list
2. With numbered items
3. Starting from 1 and incrementing

> Single line quote

```
Simple code block
```

Just a final paragraph to end things."""

    print("=== MARKDOWN BLOCK TYPE DETECTION DEMO ===\n")
    
    # Split into blocks
    blocks = markdown_to_blocks(markdown_doc)
    
    print(f"Found {len(blocks)} blocks:\n")
    
    for i, block in enumerate(blocks, 1):
        block_type = block_to_block_type(block)
        print(f"Block {i}: {block_type.value.upper()}")
        print(f"Content: {repr(block)}")
        print(f"Type: {block_type}")
        print("-" * 50)

    # Test individual examples
    print("\n=== INDIVIDUAL BLOCK TYPE TESTS ===\n")
    
    test_cases = [
        ("# Heading", "heading"),
        ("## Another Heading", "heading"), 
        ("#NotAHeading", "paragraph"),
        ("```\ncode\n```", "code"),
        (">Quote", "quote"),
        ("- List item", "unordered_list"),
        ("1. Ordered item", "ordered_list"),
        ("Normal text", "paragraph"),
    ]
    
    for block, expected in test_cases:
        detected = block_to_block_type(block)
        status = "✓" if detected.value == expected else "✗"
        print(f"{status} '{block}' → {detected.value} (expected: {expected})")

if __name__ == "__main__":
    main()
