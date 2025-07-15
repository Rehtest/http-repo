import unittest

from textnode import TextNode, TextType
from functions import split_nodes_image, split_nodes_link


class TestSplitNodesImageLink(unittest.TestCase):
    
    # Tests for split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the beginning",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Text ending with ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_entire_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This text has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Text with ![](https://i.imgur.com/zjjcJKZ.png) empty alt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" empty alt", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](https://example.com/1.png) node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second ![img2](https://example.com/2.png) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(nodes, new_nodes)

    # Tests for split_nodes_link
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_at_beginning(self):
        node = TextNode(
            "[link](https://www.boot.dev) at the beginning",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" at the beginning", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "Text ending with [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_entire_text(self):
        node = TextNode(
            "[link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This text has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_anchor_text(self):
        node = TextNode(
            "Text with [](https://www.boot.dev) empty anchor",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://www.boot.dev"),
                TextNode(" empty anchor", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](https://example.com/1) node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second [link2](https://example.com/2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(nodes, new_nodes)

    def test_split_links_with_images_nearby(self):
        # Links should ignore images
        node = TextNode(
            "A [link](https://example.com) and ![image](https://example.com/img.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and ![image](https://example.com/img.jpg)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_links_nearby(self):
        # Images should ignore links
        node = TextNode(
            "A ![image](https://example.com/img.jpg) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
                TextNode(" and [link](https://example.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    # Tests for complex scenarios
    def test_consecutive_images(self):
        node = TextNode(
            "![first](https://example.com/1.png)![second](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_consecutive_links(self):
        node = TextNode(
            "[first](https://example.com/1)[second](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com/1"),
                TextNode("second", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
