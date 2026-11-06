"""Genesis mission leaderboards, as stored in the save's `GameModeCustomBytes`.

That custom value is a union of two unrelated things. When its first byte is
`0x01` it holds the embedded player/tribe store; when it is `0x00` it holds the
per-mission leaderboards decoded here (or nothing at all, on a map that has no
missions). Nothing else in the blob distinguishes them, so a reader that assumes
one format silently misreads the other.

Each leaderboard entry is the same `FMissionScore` struct the profiles keep under
`MyData.LatestMissionScores`, which is why this module hands back the
`MissionScore` objects from `genesis1_missions` rather than a parallel type.

The one thing the binary form loses is the mission's name: the tag is reduced to
an opaque 32-bit id whose derivation is unknown (it is not any common hash of the
tag string). `resolve_tags()` recovers the names by matching entries against the
profiles, which keep the same score next to the tag as a string.
"""
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple, Union
import json
import struct

from arkparse.logging import ArkSaveLogger
from arkparse.player.genesis1_missions import Genesis1Mission, MissionScore
from arkparse.utils.json_utils import DefaultJsonEncoder

# Byte 0 of GameModeCustomBytes when the blob is the player/tribe store instead.
STORE_FLAG = 0x01
# Fixed zero header ahead of the section count.
HEADER_SIZE = 20
# The uint64 that stands in for FName("None"); NameValue is None on every entry
# seen so far, in both the leaderboard and the profile copies.
NAME_ID_NONE = 162342434
# Only Race missions score by time, where a lower value is better.
TIME_BASED_CATEGORY = "Race"


class _LeaderboardReader:
    """Minimal Unreal-style reader for the leaderboard blob."""

    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.pos = 0

    def int32(self) -> int:
        value = struct.unpack_from("<i", self.buffer, self.pos)[0]
        self.pos += 4
        return value

    def uint64(self) -> int:
        value = struct.unpack_from("<Q", self.buffer, self.pos)[0]
        self.pos += 8
        return value

    def float32(self) -> float:
        value = struct.unpack_from("<f", self.buffer, self.pos)[0]
        self.pos += 4
        return value

    def double(self) -> float:
        value = struct.unpack_from("<d", self.buffer, self.pos)[0]
        self.pos += 8
        return value

    def raw(self, count: int) -> bytes:
        value = self.buffer[self.pos:self.pos + count]
        self.pos += count
        return value

    def fstring(self) -> str:
        """Unreal FString: a positive length is UTF-8, a negative one UTF-16."""
        length = self.int32()
        if length == 0:
            return ""
        if length > 0:
            return self.raw(length)[:-1].decode("utf-8", "replace")
        return self.raw(-length * 2)[:-2].decode("utf-16-le", "replace")


@dataclass
class MissionLeaderboard:
    """The ranked scores recorded for one mission.

    `entries` is kept in file order, which is the game's own ranking: fastest
    first for time-scored missions, highest first for everything else.
    """

    mission_id: int = 0
    mission_tag: Optional[str] = None
    entries: List[MissionScore] = field(default_factory=list)

    @property
    def category(self) -> Optional[str]:
        """Hunt / Race / Escort / ... - only once the tag has been resolved."""
        if self.mission_tag is None:
            return None
        return Genesis1Mission(self.mission_tag).category

    @property
    def is_time_based(self) -> Optional[bool]:
        """True when a lower score is better, None when it cannot be decided.

        Decided from the mission category when the tag is known; otherwise
        inferred from the stored ordering, which needs at least two entries.
        """
        category = self.category
        if category is not None:
            return category == TIME_BASED_CATEGORY
        if len(self.entries) < 2:
            return None
        return self.entries[0].float_value < self.entries[-1].float_value

    @property
    def best(self) -> Optional[MissionScore]:
        """The top entry, i.e. the record holder."""
        return self.entries[0] if self.entries else None

    def rank_of(self, player_net_id: str) -> Optional[int]:
        """1-based rank of a player on this board, or None if absent."""
        for rank, entry in enumerate(self.entries, 1):
            if entry.player_net_id == player_net_id:
                return rank
        return None

    def __len__(self):
        return len(self.entries)

    def __str__(self):
        name = self.mission_tag or f"mission 0x{self.mission_id:08x}"
        return f"MissionLeaderboard({name}, {len(self.entries)} entries)"

    def to_json_obj(self):
        return {"MissionId": self.mission_id,
                "MissionTag": self.mission_tag,
                "Entries": [e.to_json_obj() for e in self.entries]}

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)


@dataclass
class MissionLeaderboards:
    """Every mission leaderboard held in one save."""

    boards: Dict[int, MissionLeaderboard] = field(default_factory=dict)

    @staticmethod
    def is_leaderboard_blob(buffer: Optional[bytes]) -> bool:
        """Whether this GameModeCustomBytes holds leaderboards rather than the
        player/tribe store. An all-zero header with no sections is a map that
        simply has none, which is not something to try to parse."""
        if not buffer or len(buffer) <= HEADER_SIZE:
            return False
        return buffer[0] != STORE_FLAG

    @classmethod
    def from_bytes(cls, buffer: Optional[bytes]) -> Optional["MissionLeaderboards"]:
        """Parse the blob, or return None if it is not a leaderboard.

        Never raises: the format is reverse-engineered, so an unexpected layout
        is reported and skipped rather than taking the caller down with it.
        """
        if not cls.is_leaderboard_blob(buffer):
            return None
        try:
            return cls._parse(bytes(buffer))
        except Exception as exc:  # noqa: BLE001 - deliberately broad, see above
            ArkSaveLogger.warning_log(
                f"GameModeCustomBytes is not a store but did not parse as mission "
                f"leaderboards either ({exc}); ignoring it")
            return None

    @classmethod
    def _parse(cls, buffer: bytes) -> "MissionLeaderboards":
        reader = _LeaderboardReader(buffer)
        reader.raw(HEADER_SIZE)
        declared = reader.int32()

        boards: Dict[int, MissionLeaderboard] = {}
        # A section is 12 bytes before its first entry, so anything shorter than
        # that left over is the trailer rather than another section.
        while reader.pos <= len(buffer) - 12:
            mission_id = reader.uint64()
            count = reader.int32()
            entries = []
            for _ in range(count):
                entry_id = reader.uint64()
                if entry_id != mission_id:
                    raise ValueError(
                        f"entry key 0x{entry_id:x} does not match section "
                        f"0x{mission_id:x} at offset {reader.pos - 8}")
                score = MissionScore()
                score.player_net_id = reader.fstring()
                score.tribe_id = reader.int32()
                score.timestamp_utc = reader.double()
                score.float_value = reader.float32()
                score.int_value = reader.int32()
                name_id = reader.uint64()
                score.name_value = "None" if name_id == NAME_ID_NONE else None
                score.string_value = reader.fstring()
                entries.append(score)
            boards[mission_id] = MissionLeaderboard(
                mission_id=mission_id, entries=entries)

        if declared != len(boards):
            ArkSaveLogger.warning_log(
                f"Mission leaderboard header declares {declared} sections but "
                f"{len(boards)} were read")
        return cls(boards=boards)

    @classmethod
    def from_save(cls, save) -> Optional["MissionLeaderboards"]:
        """Read the leaderboards straight off an AsaSave."""
        custom = save.get_custom_value("GameModeCustomBytes")
        if custom is None:
            return None
        return cls.from_bytes(bytes(custom.byte_buffer))

    def resolve_tags(self, players: Iterable) -> int:
        """Name each board by cross-referencing player profiles.

        The binary form keeps only an opaque mission id, but every profile
        records its own scores next to the mission tag as a string, so a
        (player net id, score) pair identifies the mission. Returns the number
        of boards named.

        A board stays unnamed when every score on it belongs to a player whose
        profile is no longer in the save, and is left unnamed rather than
        guessed when the pair maps to more than one mission.
        """
        by_score: Dict[Tuple[str, float], set] = {}
        for player in players:
            my_data = player.player_data.get_property_value("MyData") if player.player_data else None
            if my_data is None:
                continue
            for record in my_data.get_array_property_value("LatestMissionScores", []):
                tag = record.get_property_value("MissionTag")
                if tag is None:
                    continue
                for which in ("BestScore", "LatestScore"):
                    sub = record.get_property_value(which)
                    if sub is None:
                        continue
                    value = sub.get_property_value("FloatValue")
                    net_id = sub.get_property_value("PlayerNetId")
                    if value is None or net_id is None:
                        continue
                    by_score.setdefault((str(net_id), round(float(value), 2)), set()).add(str(tag))

        resolved = 0
        for board in self.boards.values():
            candidates = set()
            for entry in board.entries:
                hit = by_score.get((entry.player_net_id, round(entry.float_value, 2)))
                if hit:
                    candidates |= hit
            # More than one candidate means the score pair does not separate the
            # missions (Escort boards do this), so leave the board unnamed.
            if len(candidates) == 1:
                board.mission_tag = next(iter(candidates))
                for entry in board.entries:
                    entry.mission_tag = board.mission_tag
                resolved += 1
        return resolved

    def get(self, mission: Union[str, int]) -> Optional[MissionLeaderboard]:
        """Look a board up by mission id or by resolved mission tag."""
        if isinstance(mission, int):
            return self.boards.get(mission)
        for board in self.boards.values():
            if board.mission_tag == mission:
                return board
        return None

    def by_category(self, category: str) -> List[MissionLeaderboard]:
        return [b for b in self.boards.values() if b.category == category]

    def entries_of(self, player_net_id: str) -> List[Tuple[MissionLeaderboard, int, MissionScore]]:
        """Every board this player appears on, as (board, rank, score)."""
        found = []
        for board in self.boards.values():
            for rank, entry in enumerate(board.entries, 1):
                if entry.player_net_id == player_net_id:
                    found.append((board, rank, entry))
        return found

    def records_of(self, player_net_id: str) -> List[MissionLeaderboard]:
        """Boards where this player holds first place."""
        return [b for b in self.boards.values()
                if b.best is not None and b.best.player_net_id == player_net_id]

    @property
    def resolved(self) -> List[MissionLeaderboard]:
        return [b for b in self.boards.values() if b.mission_tag is not None]

    @property
    def total_entries(self) -> int:
        return sum(len(b.entries) for b in self.boards.values())

    def __len__(self):
        return len(self.boards)

    def __iter__(self):
        return iter(self.boards.values())

    def __str__(self):
        return (f"MissionLeaderboards({len(self.boards)} missions, "
                f"{self.total_entries} entries, {len(self.resolved)} named)")

    def to_json_obj(self):
        return {"Missions": [b.to_json_obj() for b in self.boards.values()]}

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)
