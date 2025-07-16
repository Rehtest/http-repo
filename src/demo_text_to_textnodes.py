"""
Demonstration of the text_to_textnodes function.
This is the culmination of all our markdown parsing work!
"""

from textnode import TextNode, TextType
from functions import text_to_textnodes

def main():
    print("=== TEXT TO TEXTNODES DEMO ===\n")
    
    # Test the exact example from the assignment
    assignment_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    
    print("Assignment example:")
    print(f"Input: {assignment_text}")
    print()
    
    result = text_to_textnodes(assignment_text)
    print("Output:")
    for i, node in enumerate(result):
        print(f"  [{i}] {repr(node)}")
    print()
    
    print("=== MORE EXAMPLES ===\n")
    
    examples = [
        "Plain text with no formatting",
        "**Bold only**",
        "_Italic only_",
        "`Code only`",
        "![Image only](https://example.com/img.png)",
        "[Link only](https://example.com)",
        "**Bold** and _italic_ together",
        "Start **bold** `code` _italic_ end",
        "**Bold**_italic_`code`![img](https://example.com/img.png)[link](https://example.com)",
        "Multiple **bold1** and **bold2** words",
        "Check ![first](https://example.com/1.png) and ![second](https://example.com/2.png) images",
        "Visit [Google](https://google.com) and [GitHub](https://github.com) sites",
    ]
    
    for example in examples:
        print(f"Input: {example}")
        nodes = text_to_textnodes(example)
        print("Output:")
        for i, node in enumerate(nodes):
            print(f"  [{i}] {repr(node)}")
        print()
    
    print("=== PROCESSING PIPELINE DEMO ===\n")
    
    # Show how the function processes step by step
    complex_text = "This is **bold** with _italic_ and `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
    
    print("Let's trace through the processing pipeline:")
    print(f"Original: {complex_text}")
    print()
    
    # Manual step-by-step (this is what happens inside text_to_textnodes)
    from functions import split_nodes_delimiter, split_nodes_image, split_nodes_link
    
    # Step 1: Start with single TEXT node
    nodes = [TextNode(complex_text, TextType.TEXT)]
    print("Step 1 - Initial:")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 2: Split bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    print("Step 2 - After bold (**):")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 3: Split italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    print("Step 3 - After italic (_):")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 4: Split code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print("Step 4 - After code (`):")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 5: Split images
    nodes = split_nodes_image(nodes)
    print("Step 5 - After images:")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 6: Split links
    nodes = split_nodes_link(nodes)
    print("Step 6 - After links:")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    # Step 7: Filter empty text nodes
    nodes = [node for node in nodes if not (node.text_type == TextType.TEXT and node.text == "")]
    print("Step 7 - After filtering empty text nodes:")
    for i, node in enumerate(nodes):
        print(f"  [{i}] {repr(node)}")
    print()
    
    print("This matches the output from text_to_textnodes()!")
    final_result = text_to_textnodes(complex_text)
    print("text_to_textnodes() result:")
    for i, node in enumerate(final_result):
        print(f"  [{i}] {repr(node)}")

if __name__ == "__main__":
    main()
