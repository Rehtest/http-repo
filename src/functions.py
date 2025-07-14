import re
from leafnode import LeafNode
from textnode import TextType, TextNode

def text_node_to_html_node(text_node) -> LeafNode:
    """
    Convert a TextNode to an HTMLNode.
    :text_node: The TextNode instance to convert.
    :return: An HTMLNode representation of the TextNode.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Unsupported text type: {text_node.text_type}")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split a list of nodes by a delimiter.
    :old_nodes: The list of nodes to split.
    :delimiter: The delimiter to split by.
    :text_type: The type of text node to create for the delimiter.
    :return: A new list of nodes with the delimiter inserted.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Only split TEXT type nodes
            new_nodes.append(node)
            continue
            
        # Split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # If there's an odd number of parts, we have unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unmatched delimiter: {delimiter}")
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Even indices are regular text (outside delimiters)
                if part:  # Only add non-empty text
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are inside delimiters
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    """
    Extract images from markdown text.
    :text: The markdown text to extract images from.
    :return: A list of tuples (alt_text, url) for each image found.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """
    Extract links from markdown text.
    :text: The markdown text to extract links from.
    :return: A list of tuples (anchor_text, url) for each link found.
    """
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)