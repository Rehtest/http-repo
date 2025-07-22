from functions import text_to_textnodes, text_node_to_html_node

text = "This paragraph has **bold**, _italic_, `code`, [a link](https://example.com), and ![an image](image.jpg) all together."

nodes = text_to_textnodes(text)
print("TextNodes:")
for i, node in enumerate(nodes):
    print(f"  {i}: {repr(node)}")

print("\nHTMLNodes:")
for i, node in enumerate(nodes):
    try:
        html_node = text_node_to_html_node(node)
        print(f"  {i}: {html_node}")
    except Exception as e:
        print(f"  {i}: ERROR - {e} - node: {repr(node)}")
