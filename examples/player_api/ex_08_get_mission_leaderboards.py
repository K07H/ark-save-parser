from arkparse.api.player_api import PlayerApi
from pathlib import Path
from arkparse.saves.asa_save import AsaSave

save_path = Path.cwd() / "temp" / "Genesis_WP.ark" # Adjust the path as needed
save = AsaSave(save_path)

player_api = PlayerApi(save)

# Only Genesis-style maps keep leaderboards; elsewhere this is empty.
if not player_api.has_mission_leaderboards():
    print("This save has no mission leaderboards")
    raise SystemExit

boards = player_api.get_mission_leaderboards()
print(f"{len(boards)} mission leaderboards, "
      f"{player_api.mission_leaderboards.total_entries} entries in total")

# Mission names are not in the leaderboard itself; they are recovered from the
# player profiles, so a board whose players have all left stays unnamed.
for board in boards[:5]:
    name = board.mission_tag or f"unnamed mission 0x{board.mission_id:08x}"
    unit = "s" if board.is_time_based else " points"
    print(f"\n{name}")
    for rank, entry in enumerate(board.entries, 1):
        print(f"  {rank:2}. {entry.string_value:20} {entry.float_value:12.2f}{unit}")

# Per player. Note most players never set a score, and the leaderboards also
# remember players whose profile is no longer in the save.
print("\nper player:")
for player in player_api.players:
    entries = player_api.get_leaderboard_entries_of(player)
    if not entries:
        continue
    records = player_api.get_leaderboard_records_of(player)
    print(f"  {player.name}: on {len(entries)} boards, {len(records)} first places")

roster = player_api.get_leaderboard_players()
gone = len(roster) - sum(1 for p in player_api.players if str(p.unique_id) in roster)
print(f"\n{len(roster)} players appear on the leaderboards, "
      f"{gone} of whom no longer have a profile in this save")
