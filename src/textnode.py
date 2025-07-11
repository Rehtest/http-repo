from enum import Enum

class TextType(Enum):
    """
    Enum representing different types of text nodes in a document.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """
    Represents a text node with a specific type and optional URL.
    """
    
    def __init__(self, text, text_type, url=None):
        """
        Initialize the TextNode with a specific value.
        :text: The value of the text node.
        :text_type: The type of the text node (must be a TextType enum value).
        :url: Optional URL for link or image text nodes.
        """
        if not isinstance(text_type, TextType):
            raise ValueError(f"text_type must be a TextType enum value, got {type(text_type)}")
        
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """
        Check equality of two TextNode instances.
        :other: The other TextNode instance to compare with.
        """
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        """
        Return a string representation of the TextNode.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"