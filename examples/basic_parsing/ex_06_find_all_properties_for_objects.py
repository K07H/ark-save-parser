from pathlib import Path
from typing import Dict
from uuid import UUID

from arkparse.saves.asa_save import AsaSave
from arkparse.api import StructureApi
from arkparse.ftp.ark_ftp_client import ArkFtpClient, ArkMap
from arkparse.object_model.ark_game_object import ArkGameObject
from arkparse.parsing import GameObjectReaderConfiguration
from arkparse.object_model.structures import StructureWithInventory

# retrieve the save file (can also retrieve it from a local path)
# save_path = ArkFtpClient.from_config(
#     Path("../../ftp_config.json"), ArkMap.LOST_COLONY).download_save_file(Path.cwd())
save_path = Path.cwd() / "LostColony_WP.ark"
save = AsaSave(save_path)

# Get object by UUID
# Example, can be part of a string or full class string
class_ = ["/Script/ShooterGame.NPCZoneManager",
          "/Script/ShooterGame.NPCZoneVolume",
          "/Game/LostColony/CoreBlueprints/Patrols/NPCZoneManager_Patrols.NPCZoneManager_Patrols_C"]
config = GameObjectReaderConfiguration(
    blueprint_name_filter=lambda name: name is not None and any(cls in name for cls in class_))  # Create filter
# Create list of generic Ark objects

objects = save.get_game_objects(config)

all_properties = set()

for key, obj in objects.items():
    all_properties.update(obj.property_names)

print(f"All properties for objects of zone objects:")
for prop in all_properties:
    print(prop)