import unittest

from functions import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    
    # Tests for extract_markdown_images
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt_text(self):
        matches = extract_markdown_images("Image with empty alt: ![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_complex_alt_text(self):
        matches = extract_markdown_images("![Complex alt text with spaces and numbers 123](https://example.com/img.jpg)")
        self.assertListEqual([("Complex alt text with spaces and numbers 123", "https://example.com/img.jpg")], matches)

    def test_extract_markdown_images_with_links_nearby(self):
        text = "Here's an image ![cat](https://example.com/cat.jpg) and a [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("cat", "https://example.com/cat.jpg")], matches)

    def test_extract_markdown_images_malformed_ignored(self):
        text = "Malformed: ![image(https://example.com/img.png) and ![good](https://example.com/good.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("good", "https://example.com/good.jpg")], matches)

    # Tests for extract_markdown_links
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("This is text with a [link](https://www.example.com)")
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_anchor_text(self):
        matches = extract_markdown_links("Link with empty text: [](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_complex_anchor_text(self):
        matches = extract_markdown_links("[Complex anchor text with spaces and numbers 123](https://example.com)")
        self.assertListEqual([("Complex anchor text with spaces and numbers 123", "https://example.com")], matches)

    def test_extract_markdown_links_with_images_nearby(self):
        text = "Here's a [link](https://example.com) and an image ![cat](https://example.com/cat.jpg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_not_confused_by_images(self):
        text = "An image ![alt text](https://example.com/img.jpg) should not be detected as a link"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_malformed_ignored(self):
        text = "Malformed: [link(https://example.com) and [good](https://example.com/good)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("good", "https://example.com/good")], matches)

    # Tests for mixed content
    def test_extract_both_images_and_links(self):
        text = "Check out this [website](https://example.com) and this ![image](https://example.com/pic.jpg)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("image", "https://example.com/pic.jpg")], images)
        self.assertListEqual([("website", "https://example.com")], links)

    def test_extract_multiple_mixed(self):
        text = "Visit [Google](https://google.com) to see ![logo](https://google.com/logo.png) or go to [YouTube](https://youtube.com) for ![videos](https://youtube.com/thumb.jpg)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [("logo", "https://google.com/logo.png"), ("videos", "https://youtube.com/thumb.jpg")]
        expected_links = [("Google", "https://google.com"), ("YouTube", "https://youtube.com")]
        
        self.assertListEqual(expected_images, images)
        self.assertListEqual(expected_links, links)

    def test_extract_nested_brackets_ignored(self):
        # Test that nested brackets are handled correctly
        text = "This [link [with] brackets](https://example.com) should work"
        matches = extract_markdown_links(text)
        # The regex should handle this correctly by not matching nested brackets
        self.assertListEqual([], matches)  # Should not match due to nested brackets

    def test_extract_special_characters_in_urls(self):
        text = "Link with query params [search](https://example.com/search?q=test&type=all)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("search", "https://example.com/search?q=test&type=all")], matches)


if __name__ == "__main__":
    unittest.main()
