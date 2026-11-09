from arkparse.api.player_api import PlayerApi
from pathlib import Path
from arkparse.saves.asa_save import AsaSave
from arkparse.player.hexagon_state import HexagonState
from arkparse.player.genesis1_missions import Genesis1Missions

save_path = Path.cwd() / "temp" / "Genesis_WP.ark" # Adjust the path as needed
save = AsaSave(save_path)

player_api = PlayerApi(save)

# The balance lives in the profile ('HexagonCount'), the pawn keeps a copy
# ('PlayerHexagonCount'). Pass the pawn too and HexagonState will check them
# against each other; the profile also covers players with no pawn in the save.
pawn_by_id = {p.get_property_value("LinkedPlayerDataID"): p for p in player_api.pawns.values()}

print("Hexagons:")
for player in sorted(player_api.players, key=lambda p: p.char_name or ""):
    hexagons = HexagonState.from_player(player, pawn_by_id.get(player.id_))
    if not hexagons.has_hexagons:
        continue

    print(f"  {player.char_name}: {hexagons.count}")
    if not hexagons.is_consistent:
        print(f"    profile and pawn disagree (pawn says {hexagons.pawn_count})")
    for milestone in hexagons.completed_spend_milestones:
        print(f"    completed spend milestone: {milestone}")

# Hexagons are earned from Genesis 1 missions, which the profile records too.
print("\nMission progress (Genesis 1):")
for player in sorted(player_api.players, key=lambda p: p.char_name or ""):
    missions = Genesis1Missions.from_player(player)
    if not missions.real_missions:
        continue

    print(f"  {player.char_name}: {len(missions.completed)}/{len(missions.real_missions)} complete, "
          f"{missions.total_glitches} glitches collected")
    for biome, found in sorted(missions.glitch_counters.items()):
        maxed = " (all found)" if biome in missions.maxed_glitch_biomes else ""
        print(f"    {biome}: {found} glitches{maxed}")

    # Every mission also keeps a best and a latest score.
    scored = [m for m in missions.real_missions if m.best_score is not None]
    if scored:
        best = max(scored, key=lambda m: m.best_score.float_value)
        print(f"    best score: {best.name} [{best.difficulty}] = {best.best_score.float_value}")
