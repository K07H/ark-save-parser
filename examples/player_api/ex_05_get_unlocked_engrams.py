from arkparse.api.player_api import PlayerApi
from pathlib import Path
from arkparse.enums.ark_map import ArkMap
from arkparse.ftp.ark_ftp_client import ArkFtpClient
from arkparse.saves.asa_save import AsaSave

save_path = ArkFtpClient.from_config(Path("../../ftp_config.json"), ArkMap.LOST_COLONY).download_save_file(Path.cwd())
save = AsaSave(save_path)

player_api = PlayerApi(save)

all_engrams = set()
for player in player_api.players:
    for eng in player.stats.engrams:
        # print(player.stats.engrams)
        all_engrams.add(eng.value)

print("Unlocked engrams:")
for engram in sorted(all_engrams):
    print(engram)
