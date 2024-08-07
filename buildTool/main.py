from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import *
from build import build_project
import os

absolute_index_file_path = os.path.abspath(input_index_file_path)
absolute_components_dir = os.path.abspath(components_dir)
absolute_styles_dir = os.path.abspath(styles_dir)
absolute_assets_dir = os.path.abspath(assets_dir)

class CustomEventHandler(LoggingEventHandler):
    def on_modified(self, event):
        # Check if the modified file is index.html
        if event.src_path == absolute_index_file_path or event.src_path.startswith(absolute_components_dir) or event.src_path.startswith(absolute_styles_dir) or event.src_path.startswith(absolute_assets_dir):
            print("Changes detected. Rebuilding...")
            build_project()   

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
