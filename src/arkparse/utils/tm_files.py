import os
from pathlib import Path
import errno
import json
from typing import Union
from uuid import uuid4

__TEMP_FILE_DIR_CLEARED = False

def __create_temp_files_folder():
    """
    Creates a folder named `asp/temp_files` under the appropriate directory
    depending on the operating system:
    - On Windows: uses LOCALAPPDATA.
    - On Linux/macOS: uses ~/.cache.
    
    Returns:
        Path: The Path object of the created directory.
    """
    if os.name == 'nt':  # Windows
        base_dir = Path(os.getenv('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    else:  # Linux/macOS
        base_dir = Path(os.getenv('XDG_CACHE_HOME', Path.home() / '.cache'))
    
    temp_files_dir = base_dir / 'asp' / 'temp_files'

    global __TEMP_FILE_DIR_CLEARED
    if not __TEMP_FILE_DIR_CLEARED:
        # Clear the temp files directory if it exists
        if temp_files_dir.exists():
            for item in temp_files_dir.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        for sub_item in item.iterdir():
                            try:
                                sub_item.unlink()
                            except OSError as e:
                                if e.errno != errno.EACCES:
                                    raise
                                # Ignore locked files
                        item.rmdir()
                except OSError as e:
                    if e.errno != errno.EACCES:
                        raise
                    # Ignore locked files
        __TEMP_FILE_DIR_CLEARED = True
        
    temp_files_dir.mkdir(parents=True, exist_ok=True)
    return temp_files_dir

TEMP_FILES_DIR = __create_temp_files_folder()

def __create_config_directory():
    """
    Creates a directory for configuration files under the temp files directory.
    
    Returns:
        Path: The Path object of the created directory.
    """
    if os.name == 'nt':  # Windows
        base_dir = Path(os.getenv('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    else:  # Linux/macOS
        base_dir = Path(os.getenv('XDG_CACHE_HOME', Path.home() / '.cache'))
    
    config_dir = base_dir / 'asp' / 'config'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

CONFIG_FILE_DIR = __create_config_directory()



def write_config_file(filename: str, content: Union[dict, list]):
    """
    Writes content to a configuration file in the config directory.
    
    Args:
        filename (str): The name of the configuration file.
        content (json): The content to write to the file.
    """
    config_file_path = CONFIG_FILE_DIR / (filename + '.json')
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(content, (dict, list)):
        raise ValueError("Content must be a dictionary or a list.")
    with open(config_file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4)

def read_config_file(filename: str) -> Union[dict, list]:
    """
    Reads content from a configuration file in the config directory.
    
    Args:
        filename (str): The name of the configuration file.
    
    Returns:
        Union[dict, list]: The content of the configuration file.
    """
    config_file_path = CONFIG_FILE_DIR / (filename + '.json')
    if not config_file_path.exists():
        return None
    
    with open(config_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_temp_file_handle(filename: str = None) -> Path:
    """
    Returns a temporary file handle in the temp files directory.
    """

    if filename is None:
        filename = uuid4().hex + '.bin'

    temp_file_path = TEMP_FILES_DIR / filename
    temp_file_path.parent.mkdir(parents=True, exist_ok=True)
    if not temp_file_path.exists():
        temp_file_path.touch()

    return temp_file_path