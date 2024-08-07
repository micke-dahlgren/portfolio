import os
import shutil
import re
import hashlib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

input_index_file_path = 'index.html'
dist_dir = './dist/'
output_index_file_path = dist_dir+'index.html'

components_dir = './components/'
component_styles_output_dir_name = 'component_styles'

styles_dir = './styles/'
assets_dir = './assets/'

absolute_index_file_path = os.path.abspath(input_index_file_path)
absolute_components_dir = os.path.abspath(components_dir)
absolute_styles_dir = os.path.abspath(styles_dir)

class CustomEventHandler(LoggingEventHandler):
    def on_modified(self, event):
        # Check if the modified file is index.html
        if event.src_path == absolute_index_file_path or event.src_path.startswith(absolute_components_dir) or event.src_path.startswith(absolute_styles_dir):
            print("Changes detected. Rebuilding...")
            build_project()            
            

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

def get_style_content(component_data):
    style_content = re.findall(r'<style[^>]*>(.*?)</style>', component_data, flags=re.DOTALL | re.MULTILINE)
    return ''.join(style_content)

def extract_html_template(content):  
    pattern = r'<template>(.*?)</template>'
    matches = re.findall(pattern, content, flags=re.DOTALL | re.MULTILINE)    
    return ''.join(matches)

def generate_unique_stylesheet_name(component_name):
    input_for_hash = component_name
    sha256_hash = hashlib.sha256(input_for_hash.encode('utf-8')).hexdigest()[:8]
    return f"{component_name}-{sha256_hash}.css"


def add_link_tag_to_index_file(index_file, stylesheet_name):
    link_tag = f'\n<link rel="stylesheet" href="./{component_styles_output_dir_name}/{stylesheet_name}" type="text/css">'
    head_start_index = index_file.find('<head>') + len('<head>')
    head_end_index = index_file.find('</head>')
    
    if head_start_index != -1 and head_end_index != -1:
        head_section = index_file[head_start_index:head_end_index].strip()
        new_head_section = head_section + link_tag
        index_file = index_file.replace(head_section, new_head_section, 1)
    else:
        raise Exception(f"No <head> tag found in input index.html file")
    print(f"Added link tag with '{stylesheet_name} to <head>'")
    return index_file

def create_stylesheet(style_content, component_name):
    stylesheet_name = generate_unique_stylesheet_name(component_name)
    output_path = f'{dist_dir}{component_styles_output_dir_name}/'
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, stylesheet_name), 'w') as stylesheet_file:
        stylesheet_file.write(style_content)
    print(f"Created '{output_path}/{stylesheet_name}'")
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
        with open(input_index_file_path, 'r') as index_file:
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
            
        
        output_html_content = '\n'.join(output_lines) # Join the processed lines back into a single string
        for stylesheet_name in stylesheets_to_append:
            output_html_content = add_link_tag_to_index_file(output_html_content, stylesheet_name)

        with open(output_index_file_path, 'w') as output_file:
            output_file.write(output_html_content)
        
        copy_directory_content(styles_dir, dist_dir)
        copy_directory_content(assets_dir, dist_dir)
        print("Build complete.")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print("Incomplete build due to missing components.")

if __name__ == "__main__":
    build_project() # initial build
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
