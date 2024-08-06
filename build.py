"""
This script is designed to build a static HTML page by replacing custom tags
in the source HTML file with the actual content of corresponding component files.
It reads an input HTML file, identifies custom tags that represent components,
and replaces these tags with the content of the corresponding component files.
If a component file does not exist, it logs a warning and leaves the tag unchanged.

Parameters:
    index_file_path (str): Path to the input HTML file containing custom tags.
    output_file_path (str): Path to the output HTML file where the final content will be written.
    components_dir (str): Directory path where component files are stored.

Assumptions:
    1. The input HTML file uses custom tags in the format '<_ComponentName>' to denote components.
    2. Each custom tag corresponds to a component file named 'ComponentName.html' in the components directory.
    3. The components directory contains all necessary component files.
    4. The script assumes a Unix-like environment for file path handling and directory creation.
"""
import os
import re
import shutil
import hashlib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

index_file_path = 'index.html'
dist_dir = './dist/'
output_file_path = dist_dir+'index.html'
components_dir = './components/'
styles_dir = './styles/'

absolute_index_file_path = os.path.abspath(index_file_path)
absolute_components_dir = os.path.abspath(components_dir)
absolute_styles_dir = os.path.abspath(styles_dir)

class CustomEventHandler(LoggingEventHandler):
    def on_modified(self, event):
        # Check if the modified file is index.html
        if event.src_path == absolute_index_file_path or event.src_path.startswith(absolute_components_dir) or event.src_path.startswith(absolute_styles_dir):
            print("Changes detected. Rebuilding...")
            build_project()

def copy_styles_to_dist():
    # Copy all .css files from the styles directory to the dist directory
    styles_dir = './styles/'
    for filename in os.listdir(styles_dir):
        if filename.endswith('.css'):
            src_file = os.path.join(styles_dir, filename)
            dst_file = os.path.join('./dist', filename)
            shutil.copy(src_file, dst_file)

def get_style_content(component_data):
    style_content = re.findall(r'<style[^>]*>(.*?)</style>', component_data, flags=re.DOTALL | re.MULTILINE)
    return ''.join(style_content)

def extract_html_template(content):
    """Extracts template content from the given HTML content."""        
    pattern = r'<template>(.*?)</template>'
    matches = re.findall(pattern, content, flags=re.DOTALL | re.MULTILINE)    
    return ''.join(matches)

def generate_unique_stylesheet_name(component_name):
    """Generates a unique stylesheet name using the component name as part of the hash input."""
    # Combine the component name with the current timestamp to ensure uniqueness
    input_for_hash = component_name
    # Use SHA256 hashing to generate a unique identifier
    sha256_hash = hashlib.sha256(input_for_hash.encode('utf-8')).hexdigest()[:8]
    # Return the hashed value as the unique stylesheet name
    return f"{component_name}-{sha256_hash}.css"

def link_stylesheet_in_head(html_content, stylesheet_path):
    """Links the given stylesheet in the HTML file's head section."""
    head_tag = re.search('<head>', html_content)
    if head_tag:
        head_content = head_tag.group(0)
        link_tag = f'<link rel="stylesheet" href="{stylesheet_path}" type="text/css">'
        return html_content.replace(head_content, head_content + link_tag)
    return html_content

def add_link_tag_to_index_file(index_file, stylesheet_name):
    # Define the link tag
    link_tag = f'\n<link rel="stylesheet" href="{stylesheet_name}" type="text/css">'
    
    # Find the start and end indices of the <head> section
    head_start_index = index_file.find('<head>') + len('<head>')
    head_end_index = index_file.find('</head>')
    
    if head_start_index != -1 and head_end_index != -1:
        # Extract the existing <head> section content excluding the opening and closing tags
        head_section = index_file[head_start_index:head_end_index].strip()
        
        # Correctly reconstruct the <head> section with the link tag included, ensuring no duplicate <head> tags
        # We do not add <head> tags here as they are already present in the original content
        new_head_section = head_section + link_tag
        
        # Replace the old <head> section content with the new one, ensuring we only replace the content and not the tags themselves
        index_file = index_file.replace(head_section, new_head_section, 1)
    else:
        raise Exception(f"No <head> tag found in input index.html file")
    
    return index_file

def create_stylesheet(style_content, component_name):
    stylesheet_name = generate_unique_stylesheet_name(component_name)
    with open(os.path.join(dist_dir, stylesheet_name), 'w') as stylesheet_file:
        stylesheet_file.write(style_content)
    return stylesheet_name

def isComponent(line):
    component_pattern = r'<_(\w+)(?:\s[^>]*)?>'
    return re.search(component_pattern, line)

def get_component_name(line):
    match = isComponent(line)
    if match:
        return match.group(1)
    raise Exception(f"Missing component match on line: \n '{line}'")

def get_component_data(component_name):
    actual_filename = os.path.join(components_dir, f"{component_name}.html")
    if not os.path.exists(actual_filename):
        raise Exception(f"Missing component: '{component_name}.html'")
    with open(actual_filename, 'r') as component_file:
        component_content = component_file.read()
    return component_content

def get_component_html_template(component_data):
    html_template = extract_html_template(component_data)
    if not html_template:        
        raise Exception("No template tag found in the provided HTML content.")
    return html_template


def build_project():
    if not os.path.exists('./dist'):
        os.makedirs('./dist')
    
    try:
        with open(index_file_path, 'r') as index_file:
            html_content = index_file.read()
        
        lines = html_content.split('\n')
        output_lines = []
        stylesheets_to_append = []
        for line in lines:
            if not isComponent(line):
                output_lines.append(line)
                continue
            try:
                # handle component html template
                component_name = get_component_name(line)
                component_data = get_component_data(component_name)
                updated_line = get_component_html_template(component_data)
                output_lines.append(updated_line)

                # handle component styles
                style_content = get_style_content(component_data)
                if style_content:
                    stylesheet_name = create_stylesheet(style_content, component_name)
                    stylesheets_to_append.append(stylesheet_name)
            except Exception as e:
                print(e)
                print("Incomplete build due to missing components.")
                return  # Exit the function early if an error occurs
        # Join the processed lines back into a single string
        output_html_content = '\n'.join(output_lines)
        for stylesheet_name in stylesheets_to_append:
            output_html_content = add_link_tag_to_index_file(output_html_content, stylesheet_name)

        with open(output_file_path, 'w') as output_file:
            output_file.write(output_html_content)
        
        copy_styles_to_dist()
        print("Build complete.")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print("Incomplete build due to missing components.")

if __name__ == "__main__":
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(absolute_components_dir), recursive=True)
    observer.schedule(event_handler, path=os.path.dirname(absolute_styles_dir), recursive=True)
    observer.schedule(event_handler, path=os.path.dirname(absolute_index_file_path), recursive=False)
    observer.start()

    try:
        while True:
            observer.join(timeout=1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()
