from enum import Enum

from arkparse.object_model.ark_game_object import ArkGameObject
from arkparse.object_model.misc.inventory_item import InventoryItem
from arkparse.parsing.ark_property_container import ArkPropertyContainer
from arkparse.api.equipment_api import EquipmentApi
from arkparse.api.dino_api import DinoApi
from arkparse.object_model.cryopods.cryopod import Cryopod
from arkparse.logging import ArkSaveLogger

class ClusterDataItemType(Enum):
    DINO = "Dino"
    EQUIPMENT = "Equipment"
    OTHER = "Other"

class ClusterDataItem:
    def __init__(self, cluster_item_data: ArkPropertyContainer, item_index: int):
        self._data = cluster_item_data
        self.version = cluster_item_data.get_property_value("Version")
        self.upload_time = cluster_item_data.get_property_value("UploadTime")
        self.item_type: ClusterDataItemType = None
        self.item: ArkGameObject = None

        if self.version != 7:
            raise ValueError(f"Unsupported cluster item data version: {self.version} for item index {item_index}")

        bp = cluster_item_data.get_property_value("ItemArchetype").value.split(' ')[1]
        ArkSaveLogger.objects_log(f"Item found with archetype {bp} and type {self.item_type}. Version: {self.version}. Upload time: {self.upload_time}.")

        # if "PrimalItem_SCSCryopod" in bp:
        #     print(cluster_item_data.to_string())
        #     input("Found cryopod item, press enter to continue...")

        if DinoApi.is_applicable_bp(bp) and (len(cluster_item_data.get_property_value("CustomItemDatas", [])) > 0):
            ArkSaveLogger.objects_log(f"Parsed as dino item with archetype: {bp}")
            self.item_type = ClusterDataItemType.DINO
            obj = ArkGameObject()
            obj.properties = cluster_item_data.properties
            self.item = Cryopod.from_object(obj, blueprint=bp)
        elif EquipmentApi.is_applicable_bp(bp):
            ArkSaveLogger.objects_log(f"Parsed as equipment item with archetype: {bp}")
            self.item_type = ClusterDataItemType.EQUIPMENT
            obj = ArkGameObject()
            obj.properties = cluster_item_data.properties
            self.item = EquipmentApi.bp_to_class(bp).from_object(obj)
        else:
            ArkSaveLogger.objects_log(f"Parsed as other item with archetype: {bp}")
            self.item_type = ClusterDataItemType.OTHER
            obj = ArkGameObject()
            obj.properties = cluster_item_data.properties
            self.item: InventoryItem = InventoryItem.from_object(obj)
            if self.item.quantity == 0:
                self.item.quantity = 1
        self.item.object.blueprint = bp

    def __str__(self):
        return f"ClusterDataItem(type={self.item_type}, item={self.item})"
        
        
    def to_json_obj(self):
        return {
            "Version": self.version,
            "UploadTime": self.upload_time,
            "Item": self.item.to_json_obj(),
            "blueprint": self.item.object.blueprint
        }

