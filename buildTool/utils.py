import re
import hashlib
from config import *


''' component parsing '''
def get_component_match(line):
    component_pattern = r'<_(\w+)(?:\s[^>]*)'
    return re.search(component_pattern, line)

def has_closing_tag(line):
    component_pattern = r'.*/>'
    return bool(re.search(component_pattern, line))

def has_component_opening_tag(line):
    component_pattern = r'^\s*<_'
    return bool(re.search(component_pattern, line))

def get_component_name(line):
    match = get_component_match(line)
    if match:
        return match.group(1)
    raise Exception(f"Missing component match on line: \n '{line}'")

def get_component_html_template(component_data):
    pattern = r'<template>(.*?)</template>'
    matches = re.findall(pattern, component_data, flags=re.DOTALL | re.MULTILINE)
    html_template = ''.join(matches)
    if not html_template:        
        raise Exception("No template tag found in the provided HTML content.")
    return html_template

def get_component_props(line):
    attr_regex = r'(\w+)="([^"]*)"'
    matches = re.findall(attr_regex, line)
    props_dict = {key: value for key, value in matches}
    if props_dict:
        return props_dict
    return {}

def insert_component_props(component_template, component_props):
    # Pattern to match keys enclosed in double curly braces {{key}}
    pattern = r"\{\{(\s*[\w\s]+?\s*)\}\}"
    
    # Iterate over each match in the component_template
    for match in re.finditer(pattern, component_template):
        propKey = match.group(1).strip()
        replaceMatch = match.group(0)
        
        if propKey in component_props:
            replacement_value = component_props[propKey]
            component_template = component_template.replace(replaceMatch, replacement_value)
        else:
            raise KeyError(f"Key '{replaceMatch}' not found in component_props")
    return component_template


def get_component_styles(component_data):
    style_content = re.findall(r'<style[^>]*>(.*?)</style>', component_data, flags=re.DOTALL | re.MULTILINE)
    return ''.join(style_content)


''' stylesheet utils '''
def generate_unique_stylesheet_name(component_name):
    input_for_hash = component_name
    sha256_hash = hashlib.sha256(input_for_hash.encode('utf-8')).hexdigest()[:8]
    return f"{component_name}-{sha256_hash}.css"

def append_stylesheet_link_tag(index_file, stylesheet_name):
    link_tag = f'\n<link rel="stylesheet" href="./{component_styles_output_dir_name}/{stylesheet_name}" type="text/css">'
    head_start_index = index_file.find('<head>') + len('<head>')
    head_end_index = index_file.find('</head>')
    
    if head_start_index != -1 and head_end_index != -1:
        head_section = index_file[head_start_index:head_end_index].strip()
        # Check if the stylesheet link already exists
        if any(link.endswith(f'="{stylesheet_name}"') for link in head_section.split('\n')):
            print(f"'{stylesheet_name}' already exists in <head>, skipping.")
            return index_file

        new_head_section = head_section + link_tag
        index_file = index_file.replace(head_section, new_head_section, 1)
    else:
        raise Exception(f"No <head> tag found in input index.html file")
    print(f"Added link tag with '{stylesheet_name} to <head>'")
    return index_file