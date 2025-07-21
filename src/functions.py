import re
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
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


def text_to_textnodes(text):
    """
    Convert raw markdown text to a list of TextNode objects.
    :text: Raw markdown text string.
    :return: List of TextNode objects with all markdown formatting parsed.
    """
    # Start with a single TEXT node containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all splitting functions in sequence
    # Order matters: bold (**) before italic (_) to avoid conflicts
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Filter out empty text nodes
    nodes = [node for node in nodes if not (node.text_type == TextType.TEXT and node.text == "")]
    
    return nodes


def markdown_to_blocks(markdown):
    """
    Split markdown text into block-level sections.
    :markdown: Raw markdown text string representing a full document.
    :return: List of block strings, with blocks separated by blank lines.
    """
    # Split by double newlines (blank lines)
    blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            # Strip trailing whitespace from each line within the block
            lines = stripped_block.split('\n')
            cleaned_lines = [line.rstrip() for line in lines]
            cleaned_blocks.append('\n'.join(cleaned_lines))
    
    return cleaned_blocks


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    :block: A single block of markdown text (whitespace already stripped).
    :return: BlockType enum representing the type of block.
    """
    lines = block.split('\n')
    
    # Check for heading (1-6 # characters followed by space)
    if block.startswith('#'):
        # Count leading # characters
        hash_count = 0
        for char in block:
            if char == '#':
                hash_count += 1
            else:
                break
        
        # Must be 1-6 # characters followed by a space
        if 1 <= hash_count <= 6 and len(block) > hash_count and block[hash_count] == ' ':
            return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith('```') and block.endswith('```') and len(block) >= 6:
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('>') for line in lines if line.strip()):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with number. followed by space, incrementing from 1)
    if lines and all(line.strip() for line in lines):  # All lines must be non-empty
        is_ordered_list = True
        for i, line in enumerate(lines):
            expected_num = i + 1
            expected_prefix = f"{expected_num}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
        
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def split_nodes_image(old_nodes):
    """
    Split nodes to extract images.
    :old_nodes: The list of nodes to process.
    :return: A new list of nodes with images extracted.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Only split TEXT type nodes
            new_nodes.append(node)
            continue
            
        # Extract all images from the text
        images = extract_markdown_images(node.text)
        if not images:
            # No images found, keep the original node
            new_nodes.append(node)
            continue
            
        # Split the text by each image found
        current_text = node.text
        for alt_text, url in images:
            # Create the full markdown image syntax
            image_markdown = f"![{alt_text}]({url})"
            
            # Split the text at the first occurrence of this image
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) == 2:
                # Add the text before the image (if not empty)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
                # Add the image node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                # Continue with the remaining text
                current_text = sections[1]
        
        # Add any remaining text after the last image
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split nodes to extract links.
    :old_nodes: The list of nodes to process.
    :return: A new list of nodes with links extracted.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # Only split TEXT type nodes
            new_nodes.append(node)
            continue
            
        # Extract all links from the text
        links = extract_markdown_links(node.text)
        if not links:
            # No links found, keep the original node
            new_nodes.append(node)
            continue
            
        # Split the text by each link found
        current_text = node.text
        for anchor_text, url in links:
            # Create the full markdown link syntax
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split the text at the first occurrence of this link
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) == 2:
                # Add the text before the link (if not empty)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
                # Add the link node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                
                # Continue with the remaining text
                current_text = sections[1]
        
        # Add any remaining text after the last link
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_children(text):
    """
    Convert markdown text to a list of HTMLNode children.
    :text: Raw markdown text string.
    :return: List of HTMLNode objects with inline formatting.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    """
    Convert a paragraph block to an HTMLNode.
    :block: The paragraph block text.
    :return: ParentNode representing a <p> tag.
    """
    # Replace newlines with spaces for paragraphs
    text = block.replace('\n', ' ')
    children = text_to_children(text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """
    Convert a heading block to an HTMLNode.
    :block: The heading block text.
    :return: ParentNode representing an <h1>-<h6> tag.
    """
    # Count the number of # characters
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    # Extract the heading text (after the # and space)
    heading_text = block[hash_count + 1:]  # +1 to skip the space
    children = text_to_children(heading_text)
    return ParentNode(f"h{hash_count}", children)


def code_to_html_node(block):
    """
    Convert a code block to an HTMLNode.
    :block: The code block text.
    :return: ParentNode representing a <pre><code> structure.
    """
    # Remove the opening and closing ```
    code_content = block[3:-3]  # Remove first 3 and last 3 characters
    
    # Strip leading/trailing newlines but preserve internal newlines
    code_content = code_content.strip('\n')
    
    # For code blocks, we don't parse inline markdown
    code_text_node = TextNode(code_content, TextType.TEXT)
    code_html_node = text_node_to_html_node(code_text_node)
    
    code_node = ParentNode("code", [code_html_node])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """
    Convert a quote block to an HTMLNode.
    :block: The quote block text.
    :return: ParentNode representing a <blockquote> tag.
    """
    lines = block.split('\n')
    # Remove the '> ' from each line
    quote_lines = []
    for line in lines:
        if line.startswith('> '):
            quote_lines.append(line[2:])  # Remove '> '
        elif line.startswith('>'):
            quote_lines.append(line[1:])  # Remove '>'
        else:
            quote_lines.append(line)
    
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """
    Convert an unordered list block to an HTMLNode.
    :block: The unordered list block text.
    :return: ParentNode representing a <ul> tag with <li> children.
    """
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        if line.startswith('- '):
            item_text = line[2:]  # Remove '- '
            item_children = text_to_children(item_text)
            list_item = ParentNode("li", item_children)
            list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """
    Convert an ordered list block to an HTMLNode.
    :block: The ordered list block text.
    :return: ParentNode representing an <ol> tag with <li> children.
    """
    lines = block.split('\n')
    list_items = []
    
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if line.startswith(expected_prefix):
            item_text = line[len(expected_prefix):]  # Remove '1. ', '2. ', etc.
            item_children = text_to_children(item_text)
            list_item = ParentNode("li", item_children)
            list_items.append(list_item)
    
    return ParentNode("ol", list_items)


class EmptyParentNode(ParentNode):
    """Special ParentNode that can be empty (for divs with no content)"""
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        props_html = self.props_to_html()
        if not self.children:
            return f"<{self.tag}{props_html}></{self.tag}>"
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    :markdown: Raw markdown text string representing a full document.
    :return: ParentNode representing a <div> containing all block elements.
    """
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # If no blocks, return empty div
    if not blocks:
        return EmptyParentNode("div", [])
    
    # Convert each block to an HTMLNode
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)
        else:
            # Default to paragraph for unknown types
            block_node = paragraph_to_html_node(block)
        
        block_nodes.append(block_node)
    
    # Wrap all blocks in a single parent div
    return ParentNode("div", block_nodes)