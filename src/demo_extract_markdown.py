"""
Demonstration of extract_markdown_images and extract_markdown_links functions.
"""

from functions import extract_markdown_images, extract_markdown_links

def main():
    # Test text with both images and links
    markdown_text = """
    # My Blog Post
    
    Check out this amazing [website](https://www.boot.dev) for learning programming!
    
    Here's a cool image: ![coding cat](https://example.com/cat-coding.gif)
    
    Also visit [YouTube](https://www.youtube.com/@bootdotdev) for videos.
    
    And here's another image: ![python logo](https://example.com/python-logo.png)
    
    Don't forget to check [GitHub](https://github.com) for open source projects!
    """
    
    print("Original markdown text:")
    print(markdown_text)
    print("\n" + "="*60 + "\n")
    
    # Extract images
    images = extract_markdown_images(markdown_text)
    print("Extracted Images:")
    if images:
        for i, (alt_text, url) in enumerate(images, 1):
            print(f"  {i}. Alt text: '{alt_text}'")
            print(f"     URL: {url}")
    else:
        print("  No images found")
    
    print("\n" + "-"*40 + "\n")
    
    # Extract links
    links = extract_markdown_links(markdown_text)
    print("Extracted Links:")
    if links:
        for i, (anchor_text, url) in enumerate(links, 1):
            print(f"  {i}. Anchor text: '{anchor_text}'")
            print(f"     URL: {url}")
    else:
        print("  No links found")
    
    print("\n" + "="*60 + "\n")
    
    # Test edge cases
    print("Testing edge cases:")
    
    edge_cases = [
        "Empty alt text: ![](https://example.com/img.png)",
        "Empty anchor text: [](https://example.com)",
        "Mixed: ![img](https://ex.com/img.jpg) and [link](https://ex.com)",
        "No markdown formatting here!",
        "Malformed: ![img(https://ex.com/img.jpg) should be ignored"
    ]
    
    for case in edge_cases:
        print(f"\nTest: {case}")
        images = extract_markdown_images(case)
        links = extract_markdown_links(case)
        print(f"  Images: {images}")
        print(f"  Links: {links}")

if __name__ == "__main__":
    main()
