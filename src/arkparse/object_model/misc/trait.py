
import os
from uuid import UUID

from arkparse import AsaSave
from arkparse.object_model.misc.inventory_item import InventoryItem
from arkparse.parsing import ArkBinaryParser

class Trait(InventoryItem):
    def __init__(self, uuid: UUID, save: AsaSave):
        super().__init__(uuid, save)

    def __str__(self):
        return super().to_string("Trait")
    
    @staticmethod
    def generate_from_template(class_: str, save: AsaSave, owner_inventory_uuid: UUID):
        uuid, _ = InventoryItem._generate(save, os.path.join("templates", "trait", "trait"))
        trait = Trait(uuid, save)
        name_id = save.save_context.get_name_id(class_) # generate name id if needed
        if name_id is None:
            save.add_name_to_name_table(class_)
        trait.replace_uuid(owner_inventory_uuid, trait.owner_inv_uuid)
        trait.reidentify(uuid, class_)
        trait.binary.replace_double(trait.object.find_property("LastAutoDurabilityDecreaseTime"), save.save_context.game_time)
        trait.update_binary()
        
        return trait
    
