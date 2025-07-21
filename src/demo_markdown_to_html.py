#!/usr/bin/env python3
"""
Demo script for markdown_to_html_node function.
Shows how to convert complete markdown documents to HTML.
"""

from functions import markdown_to_html_node

def main():
    """Demonstrate markdown to HTML conversion on various examples."""
    
    print("=== MARKDOWN TO HTML CONVERSION DEMO ===\n")
    
    # Test cases with different markdown features
    test_cases = [
        ("Simple paragraph", "This is a simple paragraph with **bold** and _italic_ text."),
        
        ("Heading", "# Main Heading\n\nThis is a paragraph under the heading."),
        
        ("Code block", """```python
def hello_world():
    print("Hello, World!")
    return True
```"""),
        
        ("Quote", """> This is a quote.
> It spans multiple lines.
> Each line starts with >."""),
        
        ("Unordered list", """- First item
- Second item with **bold**
- Third item with _italic_"""),
        
        ("Ordered list", """1. First ordered item
2. Second item with `code`
3. Third item"""),
        
        ("Mixed content", """# Complete Example

This is a **paragraph** with _italic_ text and `inline code`.

## Code Example

```javascript
function greet(name) {
    return `Hello, ${name}!`;
}
```

## Lists

### Unordered:
- Item 1
- Item 2
- Item 3

### Ordered:
1. First
2. Second  
3. Third

## Quote

> "The best way to predict the future is to invent it."
> - Alan Kay

## Links and Images

Check out [this link](https://example.com) and ![this image](image.jpg).

That's all!"""),
    ]
    
    for i, (title, markdown) in enumerate(test_cases, 1):
        print(f"{i}. {title.upper()}")
        print("Markdown:")
        print(repr(markdown))
        print("\nHTML:")
        
        try:
            node = markdown_to_html_node(markdown)
            html = node.to_html()
            print(html)
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 60)

    # Show formatted HTML for the mixed content example
    print("\n=== FORMATTED HTML EXAMPLE ===")
    
    mixed_markdown = test_cases[-1][1]  # Get the mixed content example
    node = markdown_to_html_node(mixed_markdown)
    html = node.to_html()
    
    # Simple HTML formatter (for demo purposes)
    def format_html(html):
        """Simple HTML formatter for better readability."""
        formatted = html
        # Add newlines after closing tags
        formatted = formatted.replace('></div>', '>\n</div>')
        formatted = formatted.replace('></p>', '>\n</p>')
        formatted = formatted.replace('></h1>', '>\n</h1>')
        formatted = formatted.replace('></h2>', '>\n</h2>')
        formatted = formatted.replace('></h3>', '>\n</h3>')
        formatted = formatted.replace('></ul>', '>\n</ul>')
        formatted = formatted.replace('></ol>', '>\n</ol>')
        formatted = formatted.replace('></blockquote>', '>\n</blockquote>')
        formatted = formatted.replace('></pre>', '>\n</pre>')
        # Add newlines before opening tags (except inline tags)
        formatted = formatted.replace('<h', '\n<h')
        formatted = formatted.replace('<p>', '\n<p>')
        formatted = formatted.replace('<ul>', '\n<ul>')
        formatted = formatted.replace('<ol>', '\n<ol>')
        formatted = formatted.replace('<blockquote>', '\n<blockquote>')
        formatted = formatted.replace('<pre>', '\n<pre>')
        return formatted.strip()
    
    formatted = format_html(html)
    print(formatted)

if __name__ == "__main__":
    main()
