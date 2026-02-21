from pathlib import Path
from uuid import UUID
from typing import Dict

from arkparse.api.dino_api import DinoApi, TamedDino, MapCoords
from arkparse.logging import ArkSaveLogger
from arkparse.enums import ArkMap
from arkparse.saves.asa_save import AsaSave
from arkparse.parsing.struct.actor_transform import ActorTransform

BASE_STORAGE_PATH = Path.cwd() / 'temp' / 'exports'

def create_folder(folder: str) -> None:
    """Create a folder if it does not exist."""
    path = BASE_STORAGE_PATH / folder
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

# save_path = ArkFtpClient.from_config('../../ftp_config.json', ArkMap.RAGNAROK).download_save_file(Path.cwd()) # or download the save file from an FTP server
save_path = Path.cwd() / 'Ragnarok_WP.ark'              # or use a local save file
save = AsaSave(save_path)                               # load the save file
dino_api = DinoApi(save)                                # create a DinoApi object

dinos: Dict[UUID, TamedDino] = dino_api.get_all_filtered(tamed=True, level_lower_bound=150)           # only consider tamed dinos

count = 0
for dino in dinos.values():                  # iterate over all dinos
    ArkSaveLogger.info_log(f"{dino.owner}, {dino.tamed_name}, {dino.location} ({dino.location.as_map_coords(ArkMap.RAGNAROK)})")  # print owner, name, species, level, and location
    name = dino.tamed_name if dino.tamed_name else "Unknown"
    count += 1

    print(dino.stats.stat_values.to_string_all())

    if count > 20:
        break