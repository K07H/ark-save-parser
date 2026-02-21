from enum import Enum

from arkparse.parsing.ark_property_container import ArkPropertyContainer


class ArkTributeItemType(Enum):
    Unknown = 0
    Survivor = 1
    Dinosaur = 2
    Item = 3

class ArkTributeItem:
    def __init__(self, data: ArkPropertyContainer):
        self.version: int = data.get_property_value("Version", 0)
        self.upload_time: int = data.get_property_value("UploadTime", 0)
        self.item_data: ArkPropertyContainer = data

        # tribute = data.get_property_value("ArkTributeItem", None)
        