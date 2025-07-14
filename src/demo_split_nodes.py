"""
Demonstration of using split_nodes_delimiter with multiple delimiter types.
This shows how you can chain calls to handle different markdown syntax.
"""

from textnode import TextNode, TextType
from functions import split_nodes_delimiter

def main():
    # Start with a complex markdown string
    text = "This has **bold**, _italic_, and `code` formatting in it."
    node = TextNode(text, TextType.TEXT)
    
    print("Original text:")
    print(repr(node))
    print()
    
    # Step 1: Split by ** for bold
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    print("After splitting bold (**):")
    for n in nodes:
        print(f"  {repr(n)}")
    print()
    
    # Step 2: Split by * for italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    print("After splitting italic (_):")
    for n in nodes:
        print(f"  {repr(n)}")
    print()
    
    # Step 3: Split by ` for code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    print("After splitting code (`):")
    for n in nodes:
        print(f"  {repr(n)}")
    print()
    
    print("Final result - all formatting parsed:")
    for i, n in enumerate(nodes):
        print(f"  [{i}] {repr(n)}")

if __name__ == "__main__":
    main()
