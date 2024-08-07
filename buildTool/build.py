from config import *
from utils import *
from file_operations import copy_directory_content, get_component_file_content, create_stylesheet

def build_project():    
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
                component_data = get_component_file_content(component_name)
                updated_line = get_component_html_template(component_data)
                output_lines.append(updated_line)

                # handle component styles
                style_content = get_component_styles(component_data)
                if style_content:
                    stylesheet_name = create_stylesheet(style_content, component_name)
                    stylesheets_to_append.append(stylesheet_name)
            except Exception as e:
                print(e)
                print("Incomplete build due to missing components.")
                return  # Exit the function early if an error occurs
            
        
        output_html_content = '\n'.join(output_lines) # Join the processed lines back into a single string
        for stylesheet_name in stylesheets_to_append:
            output_html_content = append_stylesheet_link_tag(output_html_content, stylesheet_name)

        with open(output_index_file_path, 'w') as output_file:
            output_file.write(output_html_content)
        
        copy_directory_content(styles_dir, dist_dir)
        copy_directory_content(assets_dir, dist_dir)
        print("Build complete.")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print("Incomplete build due to missing components.")