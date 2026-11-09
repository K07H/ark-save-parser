from arkparse.api.player_api import PlayerApi
from pathlib import Path
from arkparse.saves.asa_save import AsaSave
from arkparse.enums import AscensionSlot, AscensionLevel
from arkparse.player.ascension_data import AscensionData

save_path = Path.cwd() / "temp" / "Genesis_WP.ark" # Adjust the path as needed
save = AsaSave(save_path)

player_api = PlayerApi(save)

# Ascension is cluster-wide, so it shows up on any map's save, not just the
# one it was earned on.
pawn_by_id = {p.get_property_value("LinkedPlayerDataID"): p for p in player_api.pawns.values()}

print("Ascensions:")
for player in sorted(player_api.players, key=lambda p: p.char_name or ""):
    ascension = AscensionData.from_player(player)

    # Older profiles have no 'AscensionData' array at all; the pawn carries the
    # same levels as separately named properties and can stand in for it.
    if not ascension.has_data and player.id_ in pawn_by_id:
        ascension = AscensionData.from_pawn(pawn_by_id[player.id_])

    if not ascension.ascended_maps:
        continue

    print(f"  {player.char_name}:")
    for slot, level in ascension.ascended_maps.items():
        print(f"    {slot.name}: {level.name}")

# Individual slots can be read directly; a slot the profile is too old to have
# reads as 0 rather than raising.
print("\nPlayers who ascended on Aberration:")
for player in player_api.players:
    ascension = AscensionData.from_player(player)
    if ascension.level(AscensionSlot.ABERRATION) is not AscensionLevel.NONE:
        print(f"  {player.char_name}: {ascension.level(AscensionSlot.ABERRATION).name}")

# Slots 0-2 and 8 of the raw array have no identified meaning, so they are kept
# aside instead of being given one they may not have. A non-zero value in any of
# them logs a warning when the AscensionData is built.
print("\nUnidentified slots (raw values):")
for player in player_api.players:
    ascension = AscensionData.from_player(player)
    if ascension.has_data and any(ascension.unidentified.values()):
        print(f"  {player.char_name}: {ascension.unidentified}  (full array: {ascension.values})")
