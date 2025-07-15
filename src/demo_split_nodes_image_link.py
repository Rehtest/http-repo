"""
Demonstration of split_nodes_image and split_nodes_link functions.
"""

from textnode import TextNode, TextType
from functions import split_nodes_image, split_nodes_link

def main():
    print("=== SPLIT NODES IMAGE DEMO ===\n")
    
    # Test image splitting
    image_text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
    node = TextNode(image_text, TextType.TEXT)
    
    print("Original node:")
    print(f"  {repr(node)}")
    print()
    
    image_nodes = split_nodes_image([node])
    print("After split_nodes_image:")
    for i, n in enumerate(image_nodes):
        print(f"  [{i}] {repr(n)}")
    print()
    
    print("=== SPLIT NODES LINK DEMO ===\n")
    
    # Test link splitting
    link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    node = TextNode(link_text, TextType.TEXT)
    
    print("Original node:")
    print(f"  {repr(node)}")
    print()
    
    link_nodes = split_nodes_link([node])
    print("After split_nodes_link:")
    for i, n in enumerate(link_nodes):
        print(f"  [{i}] {repr(n)}")
    print()
    
    print("=== COMPLEX MIXED CONTENT DEMO ===\n")
    
    # Test complex mixed content
    mixed_text = "Check out this [website](https://boot.dev) and this ![cool image](https://example.com/img.png) for more info!"
    node = TextNode(mixed_text, TextType.TEXT)
    
    print("Original mixed content:")
    print(f"  {repr(node)}")
    print()
    
    # Split images first
    after_images = split_nodes_image([node])
    print("After splitting images:")
    for i, n in enumerate(after_images):
        print(f"  [{i}] {repr(n)}")
    print()
    
    # Then split links
    after_links = split_nodes_link(after_images)
    print("After splitting links:")
    for i, n in enumerate(after_links):
        print(f"  [{i}] {repr(n)}")
    print()
    
    print("=== EDGE CASES DEMO ===\n")
    
    edge_cases = [
        "![image](https://example.com/img.png)",  # Only image
        "[link](https://example.com)",  # Only link
        "![](https://example.com/img.png)",  # Empty alt text
        "[](https://example.com)",  # Empty anchor text
        "![first](https://example.com/1.png)![second](https://example.com/2.png)",  # Consecutive images
        "[first](https://example.com/1)[second](https://example.com/2)",  # Consecutive links
    ]
    
    for case in edge_cases:
        print(f"Test: {case}")
        node = TextNode(case, TextType.TEXT)
        
        # Test image splitting
        img_result = split_nodes_image([node])
        print(f"  Images: {[repr(n) for n in img_result]}")
        
        # Test link splitting
        link_result = split_nodes_link([node])
        print(f"  Links: {[repr(n) for n in link_result]}")
        print()

if __name__ == "__main__":
    main()
