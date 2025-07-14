import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        child3 = LeafNode("span", "A span")
        parent_node = ParentNode("div", [child1, child2, child3])
        expected = "<div><p>First paragraph</p><p>Second paragraph</p><span>A span</span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        result = parent_node.to_html()
        # Props order might vary, so check both possibilities
        self.assertIn('<div class="container" id="main">', result)
        self.assertIn('<span>content</span></div>', result)

    def test_to_html_with_nested_parents_and_props(self):
        grandchild = LeafNode("strong", "bold text")
        child = ParentNode("p", [grandchild], {"class": "paragraph"})
        parent = ParentNode("article", [child], {"id": "post-1", "data-type": "blog"})
        result = parent.to_html()
        self.assertIn('<article', result)
        self.assertIn('id="post-1"', result)
        self.assertIn('data-type="blog"', result)
        self.assertIn('<p class="paragraph">', result)
        self.assertIn('<strong>bold text</strong>', result)

    def test_to_html_with_mixed_node_types(self):
        # Mix of LeafNode and ParentNode children
        text_node = LeafNode("span", "Some text")
        nested_parent = ParentNode("div", [LeafNode("em", "emphasized")])
        another_text = LeafNode("p", "Another paragraph")
        
        parent = ParentNode("section", [text_node, nested_parent, another_text])
        expected = "<section><span>Some text</span><div><em>emphasized</em></div><p>Another paragraph</p></section>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_empty_props(self):
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node], {})
        self.assertEqual(parent_node.to_html(), "<div><span>content</span></div>")

    def test_to_html_with_none_props(self):
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node], None)
        self.assertEqual(parent_node.to_html(), "<div><span>content</span></div>")

    def test_to_html_raises_error_for_no_tag(self):
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node])
        parent_node.tag = None  # Manually set to None to test error
        
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have a tag", str(context.exception))

    def test_to_html_raises_error_for_no_children(self):
        parent_node = ParentNode("div", [])
        
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_to_html_raises_error_for_none_children(self):
        parent_node = ParentNode("div", [])
        parent_node.children = None  # Manually set to None to test error
        
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_complex_nested_structure(self):
        # Create a complex nested structure: article > header > h1 + nav > ul > li
        title = LeafNode("h1", "My Blog Post")
        nav_item1 = LeafNode("li", "Home")
        nav_item2 = LeafNode("li", "About")
        nav_list = ParentNode("ul", [nav_item1, nav_item2])
        nav = ParentNode("nav", [nav_list])
        header = ParentNode("header", [title, nav])
        
        content_p1 = LeafNode("p", "First paragraph of content.")
        content_p2 = LeafNode("p", "Second paragraph of content.")
        main = ParentNode("main", [content_p1, content_p2])
        
        article = ParentNode("article", [header, main], {"class": "blog-post"})
        
        result = article.to_html()
        expected_parts = [
            '<article class="blog-post">',
            '<header>',
            '<h1>My Blog Post</h1>',
            '<nav>',
            '<ul>',
            '<li>Home</li>',
            '<li>About</li>',
            '</ul>',
            '</nav>',
            '</header>',
            '<main>',
            '<p>First paragraph of content.</p>',
            '<p>Second paragraph of content.</p>',
            '</main>',
            '</article>'
        ]
        
        for part in expected_parts:
            self.assertIn(part, result)

if __name__ == "__main__":
    unittest.main()