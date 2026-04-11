from pathlib import Path
import sys
from uuid import UUID
from typing import Dict

from arkparse import AsaSave, MapCoords
from arkparse.api import StructureApi, PlayerApi
from arkparse.ftp import ArkFtpClient
from arkparse.enums import ArkMap
from arkparse.object_model.structures import StructureWithInventory

# retrieve the save file (can also retrieve it from a local path)
save_path = ArkFtpClient.from_config(Path("../../ftp_config.json"), ArkMap.LOST_COLONY).download_save_file(Path.cwd())
AsaSave(save_path).store_db(Path.cwd() / "_LostColony_WP.ark")                                                        # load the save file and store it to make sure we have a .db file to work with
save_path = Path.cwd() / "_LostColony_WP.ark"                                                               # or load it from a local path
save = AsaSave(save_path)

player_api = PlayerApi(save)
tribes = player_api.tribes
print(f"Tribes in save: {len(tribes)}")
for tribe in tribes:
    print(tribe)
ID = None # replace with the ID of the tribe you want to look for
ID = 1035108858
if ID is None:
    print("No tribe ID provided, exiting.")
    sys.exit(0)
    
structure_api = StructureApi(save)
structures: Dict[UUID, StructureWithInventory] = structure_api.get_owned_by(owner_tribe_id=ID)

print(f"Structures owned by tribe {ID}: {len(structures)}")
for structure in structures.values():
    print(structure)
    structure.set_max_health(999999999.0)
    structure.heal()

save.store_db(Path.cwd() / "LostColony_WP.ark")
