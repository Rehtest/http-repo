from typing import List, Dict, Optional

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str,
                 children: List['HTMLNode'] = [], 
                 props: Optional[Dict[str, str]] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"