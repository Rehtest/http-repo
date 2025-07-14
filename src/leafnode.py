from typing import List, Dict, Optional

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str] = None, 
                 value: Optional[str] = None, 
                 props: Optional[Dict[str, str]] = None):
        super().__init__(tag=tag, value=value, children=[], props=props)


    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag == None:
            return f"{self.value}"
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    