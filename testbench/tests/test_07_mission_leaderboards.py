"""Mission leaderboards: parse them off GameModeCustomBytes, snapshot the counts,
and check the decoded structure holds together.

Skipped entirely on a save whose GameModeCustomBytes is the player/tribe store or
is empty, which is every map without missions.
"""
import pytest

from arkparse.api import PlayerApi

from snapshot import Snapshot


@pytest.fixture(scope="module")
def player_api(save) -> PlayerApi:
    return PlayerApi(save)


@pytest.fixture(scope="module")
def leaderboards(player_api: PlayerApi):
    if not player_api.has_mission_leaderboards():
        pytest.skip("Save has no mission leaderboards")
    return player_api.mission_leaderboards


def test_loads(player_api: PlayerApi, leaderboards, snapshot: Snapshot):
    named = leaderboards.resolve_tags(player_api.players)
    print(
        f"missions={len(leaderboards)} entries={leaderboards.total_entries} "
        f"named={named}"
    )
    snapshot.check("leaderboard_missions", len(leaderboards))
    snapshot.check("leaderboard_entries", leaderboards.total_entries)
    snapshot.check("leaderboard_named", named)


def test_entries_are_well_formed(leaderboards):
    """Every decoded field has to be plausible.

    The layout is reverse-engineered, so a wrong field offset would still parse
    happily and hand back nonsense. These bounds are what nonsense would trip.
    """
    for board in leaderboards:
        assert 0 <= len(board.entries) <= 10, (
            f"board 0x{board.mission_id:08x} has {len(board.entries)} entries"
        )
        for entry in board.entries:
            assert entry.player_net_id and len(entry.player_net_id) == 32, (
                f"implausible player net id {entry.player_net_id!r}"
            )
            assert entry.string_value, "entry has no character name"
            # Timestamps must be inside the game's lifetime, not epoch-adjacent
            # garbage, which is what reading the double as an int would give.
            assert 1.4e9 < entry.timestamp_utc < 2.5e9, (
                f"implausible timestamp {entry.timestamp_utc}"
            )
            assert entry.tribe_id > 0, f"implausible tribe id {entry.tribe_id}"
            assert entry.name_value == "None", (
                f"unexpected NameValue {entry.name_value!r}"
            )


def test_boards_are_ranked(leaderboards):
    """Entries are stored in ranking order: ascending for time-scored missions
    (Race), descending for everything else."""
    checked = 0
    for board in leaderboards:
        if len(board.entries) < 2 or board.is_time_based is None:
            continue
        scores = [e.float_value for e in board.entries]
        ordered = sorted(scores) if board.is_time_based else sorted(scores, reverse=True)
        assert scores == ordered, (
            f"board {board.mission_tag or hex(board.mission_id)} is not in rank "
            f"order (time_based={board.is_time_based}): {scores}"
        )
        checked += 1
    print(f"Verified rank order on {checked} boards")
    assert checked > 0, "no board had enough entries to check ordering"


def test_only_race_missions_are_time_based(leaderboards):
    """The score is a time only for Race missions; everything else is points.
    A reader that gets this backwards reports the worst run as the record."""
    for board in leaderboards:
        if board.category is None:
            continue
        assert board.is_time_based == (board.category == "Race"), (
            f"{board.mission_tag} has category {board.category} but "
            f"is_time_based={board.is_time_based}"
        )


def test_lookup_by_tag_and_id(leaderboards, player_api: PlayerApi):
    named = [b for b in leaderboards if b.mission_tag is not None]
    if not named:
        pytest.skip("No board could be named from the profiles in this save")
    board = named[0]
    assert player_api.get_mission_leaderboard(board.mission_id) is board
    assert player_api.get_mission_leaderboard(board.mission_tag) is board


def test_player_lookup_is_consistent(player_api: PlayerApi, leaderboards):
    """A player's own entries must agree with the boards they were taken from."""
    roster = player_api.get_leaderboard_players()
    assert len(roster) > 0
    print(f"{len(roster)} distinct players across the leaderboards")

    checked = 0
    for player in player_api.players:
        entries = player_api.get_leaderboard_entries_of(player)
        for board, rank, score in entries:
            assert board.entries[rank - 1] is score
            assert score.player_net_id == str(player.unique_id)
            assert board.rank_of(score.player_net_id) <= rank
            checked += 1
        for record in player_api.get_leaderboard_records_of(player):
            assert record.best.player_net_id == str(player.unique_id)
    print(f"Verified {checked} leaderboard entries against their boards")


def test_leaderboard_is_not_the_player_list(player_api: PlayerApi, leaderboards):
    """The leaderboard roster is a historical population, not the current one.

    It is the trap this whole area sets: it looks like a plausible player list,
    which is what made returning it (or nothing) instead of the real players easy
    to miss. Assert the two are genuinely different sets so nobody wires the
    leaderboard up as a player source.
    """
    roster = set(player_api.get_leaderboard_players())
    current = {str(p.unique_id) for p in player_api.players}
    print(
        f"leaderboard roster={len(roster)} current profiles={len(current)} "
        f"overlap={len(roster & current)}"
    )
    # Everyone on a board played on this map, but their profile may be gone.
    assert roster - current, (
        "expected the leaderboards to remember players with no profile left"
    )
