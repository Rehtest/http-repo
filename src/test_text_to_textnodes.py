import unittest

from textnode import TextNode, TextType
from functions import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes_example(self):
        """Test the example from the assignment"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_plain_text(self):
        """Test with plain text (no markdown)"""
        text = "This is just plain text with no formatting"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no formatting", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_bold(self):
        """Test with only bold text"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_italic(self):
        """Test with only italic text"""
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_code(self):
        """Test with only code text"""
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_image(self):
        """Test with only image"""
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_link(self):
        """Test with only link"""
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_multiple_same_type(self):
        """Test with multiple of the same type"""
        text = "**bold1** and **bold2** and **bold3**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold3", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_bold_and_italic(self):
        """Test with both bold and italic"""
        text = "This is **bold** and _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_mixed_inline_formatting(self):
        """Test with mixed inline formatting"""
        text = "Start **bold** then `code` then _italic_ end"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_at_boundaries(self):
        """Test formatting at the beginning and end"""
        text = "**bold start** middle _italic end_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold start", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("italic end", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_consecutive_formatting(self):
        """Test consecutive formatting"""
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_empty_string(self):
        """Test with empty string"""
        text = ""
        result = text_to_textnodes(text)
        expected = []  # Empty string should result in empty list after filtering
        self.assertEqual(result, expected)

    def test_text_to_textnodes_images_and_links(self):
        """Test with both images and links"""
        text = "Check ![image](https://example.com/img.png) and [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_complex_mixed(self):
        """Test with complex mixed formatting"""
        text = "**Bold** text with `code` and _italic_ and ![img](https://example.com/img.png) and [link](https://example.com) done"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" done", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_empty_formatting(self):
        """Test with empty formatting"""
        text = "Text with **empty** and `` and ![](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("empty", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_order_matters(self):
        """Test that order of processing matters (bold before italic)"""
        # Test that ** and _ are processed correctly
        text = "This is **bold** and _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_no_empty_text_nodes(self):
        """Test that no empty text nodes are created unnecessarily"""
        text = "**bold**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_special_characters(self):
        """Test with special characters in URLs and text"""
        text = "Link with query [search](https://example.com/search?q=test&type=all) params"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Link with query ", TextType.TEXT),
            TextNode("search", TextType.LINK, "https://example.com/search?q=test&type=all"),
            TextNode(" params", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
