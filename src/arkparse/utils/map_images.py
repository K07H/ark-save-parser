from arkparse.enums import ArkMap
from importlib.resources import files

def get_map_image_file(map: ArkMap):
    package = 'arkparse.assets'
    try:
        with open(files(package) / f'{map.name}.PNG', 'rb') as img_path:
            return img_path
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the image file for the map '{map.name}', you can add it to the assets folder in the arkparse package.")