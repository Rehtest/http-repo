import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_text(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_text(self):
        node = TextNode("This is text with an _italic phrase_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_delimiters(self):
        node = TextNode("Text with `code` and more `code` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_at_beginning(self):
        node = TextNode("`code` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the beginning", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_entire_text(self):
        node = TextNode("`entire text is code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("entire text is code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter_found(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This text has no delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_delimiter_content(self):
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" empty code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code` block", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Code text", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This has unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid markdown, unmatched delimiter", str(context.exception))

    def test_multiple_unmatched_delimiters_raises_error(self):
        node = TextNode("Multiple `unmatched `delimiters `here", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Invalid markdown, unmatched delimiter", str(context.exception))

    def test_underscore_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_double_asterisk_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text_parts_filtered(self):
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_consecutive_delimiters(self):
        node = TextNode("Text with `first``second` code blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode("second", TextType.CODE),
            TextNode(" code blocks", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
