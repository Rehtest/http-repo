import os
import shutil
from textnode import TextNode, TextType
from functions import markdown_to_html_node, generate_page


def copy_static_to_public(src_path, dest_path):
    """
    Recursively copy all contents from source directory to destination directory.
    First deletes all contents of destination directory for a clean copy.
    
    :src_path: Path to the source directory
    :dest_path: Path to the destination directory
    """
    print(f"Copying static files from {src_path} to {dest_path}")
    
    # Check if source directory exists
    if not os.path.exists(src_path):
        print(f"Error: Source directory {src_path} does not exist")
        return
    
    if not os.path.isdir(src_path):
        print(f"Error: {src_path} is not a directory")
        return
    
    # First, delete all contents of the destination directory if it exists
    if os.path.exists(dest_path):
        print(f"Removing existing directory: {dest_path}")
        shutil.rmtree(dest_path)
    
    # Create the destination directory
    print(f"Creating directory: {dest_path}")
    os.mkdir(dest_path)
    
    # Copy all contents recursively
    _copy_directory_contents(src_path, dest_path)


def _copy_directory_contents(src_path, dest_path):
    """
    Helper function to recursively copy directory contents.
    
    :src_path: Path to the source directory
    :dest_path: Path to the destination directory
    """
    # List all items in the source directory
    for item in os.listdir(src_path):
        src_item_path = os.path.join(src_path, item)
        dest_item_path = os.path.join(dest_path, item)
        
        if os.path.isfile(src_item_path):
            # If it's a file, copy it
            print(f"Copying file: {src_item_path} -> {dest_item_path}")
            shutil.copy(src_item_path, dest_item_path)
        else:
            # If it's a directory, create it and recursively copy its contents
            print(f"Creating directory: {dest_item_path}")
            os.mkdir(dest_item_path)
            _copy_directory_contents(src_item_path, dest_item_path)


def generate_pages_recursive(content_dir, template_path, dest_dir):
    """
    Recursively generate HTML pages from all markdown files in content directory.
    
    :content_dir: Path to the content directory containing markdown files
    :template_path: Path to the HTML template file
    :dest_dir: Path to the destination directory for HTML files
    """
    # Check if content directory exists
    if not os.path.exists(content_dir):
        print(f"Error: Content directory {content_dir} does not exist")
        return
    
    # Process all items in the content directory
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        
        if os.path.isfile(item_path) and item.endswith('.md'):
            # It's a markdown file - convert it to HTML
            relative_path = os.path.relpath(item_path, content_dir)
            html_filename = os.path.splitext(relative_path)[0] + '.html'
            dest_html_path = os.path.join(dest_dir, html_filename)
            
            # Create destination directory if it doesn't exist
            dest_html_dir = os.path.dirname(dest_html_path)
            if dest_html_dir and not os.path.exists(dest_html_dir):
                os.makedirs(dest_html_dir)
            
            print(f"Generating page: {item_path} -> {dest_html_path}")
            generate_page(item_path, template_path, dest_html_path)
            
        elif os.path.isdir(item_path):
            # It's a directory - recursively process it
            dest_subdir = os.path.join(dest_dir, item)
            generate_pages_recursive(item_path, template_path, dest_subdir)


def main():
    """
    Main function to generate the static site.
    """
    print("Starting static site generation...")
    
    # Get the current directory (src) and project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define paths
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")
    content_path = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    # Delete anything in the public directory (for clean generation)
    if os.path.exists(public_path):
        print(f"Removing existing public directory: {public_path}")
        shutil.rmtree(public_path)
    
    # Copy static files to public directory
    copy_static_to_public(static_path, public_path)
    
    # Generate all pages recursively from content directory
    generate_pages_recursive(content_path, template_path, public_path)
    
    print("Static site generation completed!")


if __name__ == "__main__":
    main()