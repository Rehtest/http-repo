import unittest
import tempfile
import os
import shutil
from functions import generate_page


class TestGeneratePage(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures with temporary directories."""
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
    
    def test_generate_simple_page(self):
        """Test generating a simple HTML page from markdown."""
        # Create test markdown file
        md_content = "# Test Page\n\nThis is a **test** page."
        md_path = os.path.join(self.test_dir, "test.md")
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        # Create test template
        template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        # Generate page
        dest_path = os.path.join(self.test_dir, "output.html")
        generate_page(md_path, template_path, dest_path)
        
        # Check that output file was created
        self.assertTrue(os.path.exists(dest_path))
        
        # Check content
        with open(dest_path, 'r') as f:
            result = f.read()
        
        self.assertIn("<title>Test Page</title>", result)
        self.assertIn("<h1>Test Page</h1>", result)
        self.assertIn("<b>test</b>", result)
    
    def test_generate_page_creates_directories(self):
        """Test that generate_page creates necessary directories."""
        # Create test files
        md_content = "# Test\n\nContent"
        md_path = os.path.join(self.test_dir, "test.md")
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        # Generate page in nested directory that doesn't exist
        dest_path = os.path.join(self.test_dir, "nested", "deep", "output.html")
        generate_page(md_path, template_path, dest_path)
        
        # Check that file was created and directories were created
        self.assertTrue(os.path.exists(dest_path))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "nested", "deep")))
    
    def test_generate_page_complex_markdown(self):
        """Test generating page with complex markdown content."""
        md_content = """# Main Title

## Subtitle

Here's some text with **bold** and _italic_.

- List item 1
- List item 2

```python
print("code block")
```

> This is a quote

[Link text](http://example.com)

![Image alt](image.jpg)"""
        
        md_path = os.path.join(self.test_dir, "complex.md")
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        template_content = """<!doctype html>
<html>
<head><title>{{ Title }}</title></head>
<body><article>{{ Content }}</article></body>
</html>"""
        template_path = os.path.join(self.test_dir, "template.html")
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        dest_path = os.path.join(self.test_dir, "complex.html")
        generate_page(md_path, template_path, dest_path)
        
        with open(dest_path, 'r') as f:
            result = f.read()
        
        # Check title extraction
        self.assertIn("<title>Main Title</title>", result)
        
        # Check various HTML elements are present
        self.assertIn("<h1>Main Title</h1>", result)
        self.assertIn("<h2>Subtitle</h2>", result)
        self.assertIn("<b>bold</b>", result)
        self.assertIn("<i>italic</i>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<li>List item 1</li>", result)
        self.assertIn("<pre><code>", result)
        self.assertIn('print("code block")', result)
        self.assertIn("<blockquote>", result)
        self.assertIn('<a href="http://example.com">Link text</a>', result)
        self.assertIn('<img src="image.jpg" alt="Image alt"', result)


if __name__ == "__main__":
    unittest.main()
