from pathlib import Path
from arkparse.parsing.ark_archive import ArkArchive
from arkparse.logging import ArkSaveLogger
from arkparse.parsing.ark_property_container import set_print_depth
from arkparse.object_model.cluster_data.ark_cluster_data import ClusterData
from arkparse.api.player_api import PlayerApi
ArkSaveLogger.set_log_level(ArkSaveLogger.LogTypes.ALL, False)

from arkparse.api.player_api import PlayerApi
from pathlib import Path
from arkparse.saves.asa_save import AsaSave

save_path = Path.cwd() / "_Ragnarok_WP.ark" # Adjust the path as needed
save = AsaSave(save_path)

player_api = PlayerApi(save, cluster_data_dir=Path.cwd() / "cluster_data") # when a path is provided, the lib will parse all files in that dir as cluster data and match them to players by uuid
player_api = PlayerApi(save) # lib will search for cluster data in the same folder as the save by default, but only when cluster data files are named with the player's uuid and have no extension

for filename, cluster_data in player_api.cluster_data.items():
    print(f"\n=== Cluster Data for id {filename}: ===")
    print("\nItems:")
    for item in cluster_data.items:
        print(item)

    print("\nDinos:")
    for dino in cluster_data.dinos:
        print(dino)
