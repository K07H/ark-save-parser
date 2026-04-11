from pathlib import Path
from uuid import UUID
from typing import Dict
import json

from arkparse import AsaSave
from arkparse.api import StructureApi, PlayerApi
from arkparse.ftp import ArkFtpClient
from arkparse.enums import ArkMap
from arkparse.object_model.structures import Structure
from arkparse.parsing.struct.actor_transform import MapCoords

digits = 1

# retrieve the save file (can also retrieve it from a local path)
save_path = ArkFtpClient.from_config(Path("../../ftp_config.json"), ArkMap.RAGNAROK).download_save_file(Path.cwd())
save = AsaSave(save_path)

json_data = {}

structure_api = StructureApi(save)
player_api = PlayerApi(save)
all_structures: Dict[UUID, Structure] = structure_api.get_all()

for key, val in all_structures.items():
    owner_id = val.owner.tribe_id
    if owner_id is None or val.location is None:
        continue
    if val.owner.tribe_name is not None:
        tribe_name = val.owner.tribe_name
    else:
        tribe = player_api.get_tribe(owner_id)
        tribe_name = tribe.name if tribe is not None else str(owner_id)

    if tribe_name not in json_data and tribe_name is not None:
        json_data[tribe_name] = {}

    coords: MapCoords = val.location.as_map_coords(ArkMap.RAGNAROK)
    coords.round(digits)
    coords_key = f"{coords.lat:.1f},{coords.long:.1f}"
    if coords_key not in json_data[tribe_name]:
        json_data[tribe_name][coords_key] = {
            "name":val.get_short_name()
        }
    else:
        if "name" in json_data[tribe_name][coords_key]:
            del json_data[tribe_name][coords_key]["name"]
        json_data[tribe_name][coords_key]["count"] = json_data[tribe_name][coords_key].get("count", 1) + 1


print(f"Found {len(all_structures)} structures, owned by {len(json_data)} tribes")
print(json.dumps(json_data, indent=4))
