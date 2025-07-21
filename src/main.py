import os
import shutil
from textnode import TextNode, TextType
from functions import markdown_to_html_node


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


def main():
    # Get the root project directory (parent of src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Define source and destination paths
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")
    
    # Copy static files to public directory
    copy_static_to_public(static_path, public_path)
    
    print("Static site generation completed!")


if __name__ == "__main__":
    main()