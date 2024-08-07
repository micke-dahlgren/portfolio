import re
import hashlib
from config import *

def isComponent(line):
    component_pattern = r'<_(\w+)(?:\s[^>]*)?>'
    return re.search(component_pattern, line)


def get_component_name(line):
    match = isComponent(line)
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


def get_component_styles(component_data):
    style_content = re.findall(r'<style[^>]*>(.*?)</style>', component_data, flags=re.DOTALL | re.MULTILINE)
    return ''.join(style_content)


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
        new_head_section = head_section + link_tag
        index_file = index_file.replace(head_section, new_head_section, 1)
    else:
        raise Exception(f"No <head> tag found in input index.html file")
    print(f"Added link tag with '{stylesheet_name} to <head>'")
    return index_file