import unittest
from functions import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test paragraph conversion with inline formatting"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Test code block conversion (no inline formatting)"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_headings(self):
        """Test all heading levels"""
        md = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_headings_with_inline_formatting(self):
        """Test headings with inline formatting"""
        md = "# This is a **bold** heading with _italic_ text"

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>This is a <b>bold</b> heading with <i>italic</i> text</h1></div>"
        self.assertEqual(html, expected)
    
    def test_quote_blocks(self):
        """Test quote block conversion"""
        md = """> This is a quote
> It spans multiple lines
> Each line starts with >"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote\nIt spans multiple lines\nEach line starts with ></blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_quote_with_inline_formatting(self):
        """Test quote with inline formatting"""
        md = "> This quote has **bold** and _italic_ text"

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This quote has <b>bold</b> and <i>italic</i> text</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        """Test unordered list conversion"""
        md = """- First item
- Second item
- Third item"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list_with_inline_formatting(self):
        """Test unordered list with inline formatting"""
        md = """- Item with **bold** text
- Item with _italic_ text
- Item with `code`"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>Item with <b>bold</b> text</li><li>Item with <i>italic</i> text</li><li>Item with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        md = """1. First item
2. Second item
3. Third item"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list_with_inline_formatting(self):
        """Test ordered list with inline formatting"""
        md = """1. Item with **bold** text
2. Item with _italic_ text
3. Item with `code`"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>Item with <b>bold</b> text</li><li>Item with <i>italic</i> text</li><li>Item with <code>code</code></li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_mixed_content(self):
        """Test a document with multiple block types"""
        md = """# Main Title

This is a paragraph with **bold** text.

## Subtitle

> A quote with _italic_ text

- List item 1
- List item 2

1. Ordered item 1
2. Ordered item 2

```
def code_example():
    return "no **formatting** here"
```

Final paragraph."""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Verify it starts with <div> and ends with </div>
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
        
        # Verify it contains all the expected elements
        self.assertIn("<h1>Main Title</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text.</p>", html)
        self.assertIn("<h2>Subtitle</h2>", html)
        self.assertIn("<blockquote>A quote with <i>italic</i> text</blockquote>", html)
        self.assertIn("<ul><li>List item 1</li><li>List item 2</li></ul>", html)
        self.assertIn("<ol><li>Ordered item 1</li><li>Ordered item 2</li></ol>", html)
        self.assertIn("<pre><code>def code_example():\n    return \"no **formatting** here\"</code></pre>", html)
        self.assertIn("<p>Final paragraph.</p>", html)
    
    def test_empty_markdown(self):
        """Test empty markdown"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div></div>"
        self.assertEqual(html, expected)
    
    def test_whitespace_only(self):
        """Test markdown with only whitespace"""
        md = "   \n\n   "
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div></div>"
        self.assertEqual(html, expected)
    
    def test_complex_inline_formatting(self):
        """Test paragraph with complex inline formatting including links and images"""
        md = "This paragraph has **bold**, _italic_, `code`, [a link](https://example.com), and ![an image](image.jpg) all together."

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><p>This paragraph has <b>bold</b>, <i>italic</i>, <code>code</code>, <a href="https://example.com">a link</a>, and <img src="image.jpg" alt="an image"></img> all together.</p></div>'
        self.assertEqual(html, expected)

if __name__ == "__main__":
    unittest.main()
