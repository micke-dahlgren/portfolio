import os 
import shutil
from config import *
from utils import generate_unique_stylesheet_name

def get_component_file_content(component_name):
    actual_filename = os.path.join(components_dir, f"{component_name}.html")
    if not os.path.exists(actual_filename):
        raise Exception(f"Missing component: '{component_name}.html'")
    with open(actual_filename, 'r') as component_file:
        component_content = component_file.read()
    return component_content

def copy_directory_content(source, destination):
    # Ensure the source directory exists
    if not os.path.exists(source):
        raise FileNotFoundError(f"The source directory '{source}' does not exist.")
    
    # Get the name of the source directory
    source_dir_name = os.path.basename(os.path.normpath(source))
    
    # Create the full path for the new directory in the destination
    new_dir_path = os.path.join(destination, source_dir_name)
    
    # If the destination directory already exists, delete it
    if os.path.exists(new_dir_path):
        shutil.rmtree(new_dir_path)
    
    # Create the new directory
    os.makedirs(new_dir_path)
    
    # Copy all content from source to new directory in destination
    for item in os.listdir(source):
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(new_dir_path, item)
        
        if os.path.isdir(source_item_path):
            shutil.copytree(source_item_path, destination_item_path)
        else:
            shutil.copy2(source_item_path, destination_item_path)
    
    print(f"Copied content from '{source}' to '{new_dir_path}'.")

def create_stylesheet(style_content, component_name):
    stylesheet_name = generate_unique_stylesheet_name(component_name)
    output_path = f'{dist_dir}{component_styles_output_dir_name}/'
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, stylesheet_name), 'w') as stylesheet_file:
        stylesheet_file.write(style_content)
    print(f"Created '{output_path}/{stylesheet_name}'")
    return stylesheet_name