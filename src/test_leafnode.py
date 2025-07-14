import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_value(self):
        node = LeafNode(tag="p", value="This is a leaf node", props={"class": "test"})
        expected_html = '<p class="test">This is a leaf node</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_value(self):
        node = LeafNode(tag="span")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_without_tag(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")