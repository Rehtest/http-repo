import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init_with_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_init_with_values(self):
        children = [HTMLNode(tag="child1"), HTMLNode(tag="child2")]
        props = {"class": "test", "id": "node1"}
        node = HTMLNode(tag="div", value="Content", children=children, props=props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_repr(self):
        node = HTMLNode(tag="span", value="Hello", props={"style": "color: red"})
        expected_repr = "HTMLNode(tag=span, value=Hello, children=None, props={'style': 'color: red'})"
        self.assertEqual(repr(node), expected_repr)