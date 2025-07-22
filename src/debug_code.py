from functions import markdown_to_blocks, markdown_to_html_node

md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

blocks = markdown_to_blocks(md)
print("Blocks:", blocks)
for i, block in enumerate(blocks):
    print(f"Block {i}: {repr(block)}")

print("\n" + "="*50)
node = markdown_to_html_node(md)
html = node.to_html()
print("HTML:", html)
