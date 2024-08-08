from config import *
from utils import *
import htmlmin

from file_operations import copy_directory_content, get_component_file_content, create_stylesheet

class ComponentData:
    def __init__(self, name, props, file_content, template):
        self.name = name
        self.props = props
        self.file_content = file_content
        self.template = template
    def reset(self):
        self.name = ""
        self.props = {}
        self.file_content = ""
        self.template = ""

class StylesheetData:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def reset(self):
        self.id = ""
        self.content = ""




def build_project():    
    try:
        with open(input_index_file_path, 'r') as index_file:
            html_content = index_file.read()
        
        lines = html_content.split('\n')
        output_lines = []
        stylesheets_to_append = []
        component = ComponentData(
            name="",
            props={},
            file_content="",
            template="",
        )
        stylesheet = StylesheetData(
             id="",
             content="",
        )

        doParse = False
        for line in lines:
            
            hasComponentOpeningTag = has_component_opening_tag(line)
            hasClosingTag = has_closing_tag(line)
            if hasComponentOpeningTag:
                doParse = True

            if not doParse:
                output_lines.append(line)
                continue
            
            try:
                # parse component
                if hasComponentOpeningTag:
                    component.name = get_component_name(line)
                    component.file_content = get_component_file_content(component.name)
                    
                component.props = {**component.props, **get_component_props(line)}
                
                if doParse and hasClosingTag:
                    if component.props:
                        component.file_content = insert_component_props(component.file_content, component.props)
                    component.template = get_component_html_template(component.file_content)
                    output_lines.append(component.template)
                    # handle component styles
                    stylesheet.content = get_component_styles(component.file_content)
                    if stylesheet.content:
                        stylesheet.id = create_stylesheet(stylesheet.content, component.name)
                        stylesheets_to_append.append(stylesheet.id)
                    stylesheet.reset()
                    component.reset()
                    doParse = False
            except Exception as e:
                print(e)
                print("Incomplete build due to missing components.")
                return  # Exit the function early if an error occurs
            
        
        output_html_content = '\n'.join(output_lines) # Join the processed lines back into a single string
        for stylesheet_name in stylesheets_to_append:
            output_html_content = append_stylesheet_link_tag(output_html_content, stylesheet_name)

        with open(output_index_file_path, 'w') as output_file:
            if config['minify']:
                output_html_content = htmlmin.minify(output_html_content, remove_empty_space=True)
            output_file.write(output_html_content)
        
        copy_directory_content(styles_dir, dist_dir)
        copy_directory_content(assets_dir, dist_dir)
        print("Build complete.")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        print("Incomplete build due to missing components.")