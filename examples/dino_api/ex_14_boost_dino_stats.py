from pathlib import Path
from typing import Dict
from uuid import UUID
import sys

from arkparse.enums.ark_stat import ArkStat
from arkparse.ftp.ark_ftp_client import ArkFtpClient, ArkMap
from arkparse.api.dino_api import DinoApi
from arkparse.saves.asa_save import AsaSave
from arkparse.object_model.dinos import TamedDino
from arkparse.api import PlayerApi
from arkparse import Classes

save_path = ArkFtpClient.from_config('../../ftp_config.json', ArkMap.LOST_COLONY).download_save_file(Path.cwd())   # or download the save file from an FTP server
AsaSave(save_path).store_db(Path.cwd() / "_LostColony_WP.ark")                                                        # load the save file and store it to make sure we have a .db file to work with
save_path = Path.cwd() / "_LostColony_WP.ark"                                                               # or load it from a local path
save = AsaSave(save_path)                                                                                       # load the save file
dino_api = DinoApi(save)                                                                                        # create a DinoApi object
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

tribe = player_api.get_tribe(ID)
dinos_in_tribe = dino_api.get_owned_by_tribe(ID)
print(f"Dinos in tribe {tribe.name} (ID: {tribe.tribe_id}): {len(dinos_in_tribe)}")
for dino in dinos_in_tribe.values():
    print(dino)
    print("Restoring stats...")
    dino.heal()
    dino.feed()

    print("Setting health and melee damage levels to 255... (255=max)")
    dino.stats.set_tamed_levels(255, ArkStat.HEALTH)
    dino.stats.set_tamed_levels(255, ArkStat.MELEE_DAMAGE)
    dino.stats.set_levels(255, ArkStat.HEALTH)
    dino.stats.set_levels(255, ArkStat.MELEE_DAMAGE)

    print("Set health and melee damage to max levels healed the dino.")

save.store_db(Path.cwd() / "LostColony_WP.ark")