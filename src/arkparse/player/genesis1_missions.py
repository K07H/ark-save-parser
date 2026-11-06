import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TYPE_CHECKING

from arkparse.parsing import ArkPropertyContainer
from arkparse.utils.json_utils import DefaultJsonEncoder

if TYPE_CHECKING:
    from arkparse.player.ark_player import ArkPlayer

# The buff object that carries per-mission completion in a Genesis 1 profile.
MISSION_BUFF_CLASS = "/Script/ShooterGame.PrimalBuffPersistentData_MissionData"
MISSION_BUFF_BLUEPRINT = "/Game/Genesis/Missions/Buff_MissionData.Buff_MissionData_C"

# /Game/Genesis/Missions/Escort/MissionType_Escort_Bog_Toad_Hard.MissionType_Escort_Bog_Toad_Hard_C
MISSION_TAG_PATTERN = re.compile(r"/Game/Genesis2?/Missions/(?P<path>.*?)/?MissionType_(?P<name>[^/.]+)\.")

DIFFICULTIES = ("Easy", "Medium", "Hard")
BIOMES = ("Arctic", "Bog", "Lunar", "Ocean", "Volcanic")


@dataclass
class MissionScore:
    """One half of a LatestMissionScores entry (either BestScore or LatestScore)."""

    mission_tag: Optional[str] = None
    float_value: float = 0.0
    int_value: int = 0
    name_value: Optional[str] = None
    string_value: Optional[str] = None
    player_net_id: Optional[str] = None
    tribe_id: Optional[int] = None
    timestamp_utc: Optional[float] = None

    def __init__(self, properties: Optional[ArkPropertyContainer] = None):
        if properties is None:
            return
        self.mission_tag = properties.get_property_value("MissionTag")
        self.float_value = properties.get_property_value("FloatValue", 0.0)
        self.int_value = properties.get_property_value("IntValue", 0)
        self.name_value = properties.get_property_value("NameValue")
        self.string_value = properties.get_property_value("StringValue")
        self.player_net_id = properties.get_property_value("PlayerNetId")
        self.tribe_id = properties.get_property_value("TribeID")
        self.timestamp_utc = properties.get_property_value("TimestampUtc")

    def __str__(self):
        return (f"MissionScore(score={self.float_value}, int={self.int_value}, "
                f"by={self.string_value}, tribe={self.tribe_id}, at={self.timestamp_utc})")

    def to_json_obj(self):
        return { "MissionTag": self.mission_tag,
                 "FloatValue": self.float_value,
                 "IntValue": self.int_value,
                 "NameValue": self.name_value,
                 "StringValue": self.string_value,
                 "PlayerNetId": self.player_net_id,
                 "TribeID": self.tribe_id,
                 "TimestampUtc": self.timestamp_utc }

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)


@dataclass
class Genesis1Mission:
    """A single Genesis 1 mission as recorded in a player profile.

    Completion comes from the mission buff's MissionData array, where each
    entry is a MissionTag plus a JSON blob. Scores come from a separate array
    (MyData.LatestMissionScores) and are matched back on the tag, so either
    half can be missing.
    """

    tag: str = ""
    category: Optional[str] = None       # Hunt, Escort, Race, VRBattle, GlitchCounter, ...
    name: Optional[str] = None           # Escort_Bog_Toad, with the difficulty stripped
    difficulty: Optional[str] = None     # Easy / Medium / Hard, None when the mission has no tiers
    biome: Optional[str] = None          # Arctic / Bog / Lunar / Ocean / Volcanic

    complete: bool = False
    completed_at: Optional[float] = None  # unix seconds
    version: Optional[int] = None
    glitches_collected: Optional[int] = None

    serialized_data: Dict = field(default_factory=dict)
    best_score: Optional[MissionScore] = None
    latest_score: Optional[MissionScore] = None

    def __init__(self, tag: str, serialized_data: str = None):
        self.tag = tag
        self.category, self.name, self.difficulty, self.biome = self._parse_tag(tag)

        self.serialized_data = {}
        if serialized_data:
            try:
                self.serialized_data = json.loads(serialized_data)
            except (ValueError, TypeError):
                # Keep the raw blob rather than dropping the mission entirely.
                self.serialized_data = {"raw": serialized_data}

        self.complete = bool(self.serialized_data.get("complete", False))
        self.completed_at = self.serialized_data.get("completeutctime")
        self.version = self.serialized_data.get("version")
        # Only the per-biome glitch counters carry this.
        self.glitches_collected = self.serialized_data.get("completeglitches")

        self.best_score = None
        self.latest_score = None

    @staticmethod
    def _parse_tag(tag: str):
        match = MISSION_TAG_PATTERN.match(tag or "")
        if not match:
            return None, None, None, None

        path = match.group("path")
        name = match.group("name")

        # Missions sit in a category folder (Hunt/Ocean/...); the glitch counters
        # sit directly in Missions/, so fall back to the name itself.
        category = path.split("/")[0] if path else None
        if not category:
            category = "GlitchCounter" if name.startswith("GlitchCounter") else None

        difficulty = None
        for tier in DIFFICULTIES:
            if name.endswith("_" + tier):
                difficulty = tier
                name = name[: -(len(tier) + 1)]
                break

        biome = next((b for b in BIOMES if b in name or b in path), None)

        return category, name, difficulty, biome

    @property
    def is_glitch_counter(self) -> bool:
        """The five per-biome glitch trackers are stored as pseudo-missions."""
        return self.category == "GlitchCounter"

    def __str__(self):
        state = f"glitches={self.glitches_collected}" if self.is_glitch_counter else (
            "complete" if self.complete else "incomplete")
        difficulty = f" [{self.difficulty}]" if self.difficulty else ""
        return f"Genesis1Mission({self.name}{difficulty}, {state})"

    def to_json_obj(self):
        return { "MissionTag": self.tag,
                 "Category": self.category,
                 "Name": self.name,
                 "Difficulty": self.difficulty,
                 "Biome": self.biome,
                 "Complete": self.complete,
                 "CompleteUtcTime": self.completed_at,
                 "Version": self.version,
                 "CompleteGlitches": self.glitches_collected,
                 "SerializedData": self.serialized_data,
                 "BestScore": self.best_score.to_json_obj() if self.best_score is not None else None,
                 "LatestScore": self.latest_score.to_json_obj() if self.latest_score is not None else None }

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)


@dataclass
class Genesis1Missions:
    """All Genesis 1 mission progress held in a player profile.

    Merges the two places the profile keeps it:
      * the PrimalBuffPersistentData_MissionData buff - ActiveMissionIndex and
        a MissionData array of (MissionTag, SerializedData JSON)
      * MyData.LatestMissionScores - per-mission best and latest score

    Missions seen only in the score array still get an entry, with complete
    left False.
    """

    active_mission_index: int = -1
    missions: Dict[str, Genesis1Mission] = field(default_factory=dict)

    def __init__(self, mission_buff: Optional[ArkPropertyContainer] = None,
                 my_data: Optional[ArkPropertyContainer] = None):
        self.active_mission_index = -1
        self.missions = {}

        if mission_buff is not None:
            self.active_mission_index = mission_buff.get_property_value("ActiveMissionIndex", -1)
            for entry in mission_buff.get_array_property_value("MissionData", []):
                tag = entry.get_property_value("MissionTag")
                if tag is None:
                    continue
                self.missions[tag] = Genesis1Mission(tag, entry.get_property_value("SerializedData"))

        if my_data is not None:
            for entry in my_data.get_array_property_value("LatestMissionScores", []):
                tag = entry.get_property_value("MissionTag")
                if tag is None:
                    continue
                mission = self.missions.get(tag)
                if mission is None:
                    mission = Genesis1Mission(tag)
                    self.missions[tag] = mission
                best = entry.get_property_value("BestScore")
                latest = entry.get_property_value("LatestScore")
                mission.best_score = MissionScore(best) if best is not None else None
                mission.latest_score = MissionScore(latest) if latest is not None else None

    @classmethod
    def from_player(cls, player: "ArkPlayer") -> "Genesis1Missions":
        buff = player._archive.get_object_by_class(MISSION_BUFF_CLASS)
        if buff is None:
            # Older archives file the buff under the generic class instead.
            buff = next((obj for obj in player._archive.objects
                         if obj.get_property_value("ForPrimalBuffClassString") == MISSION_BUFF_BLUEPRINT), None)
        return cls(buff, player.player_data.get_property_value("MyData"))

    @property
    def real_missions(self) -> List[Genesis1Mission]:
        """Actual missions, without the five per-biome glitch counters."""
        return [m for m in self.missions.values() if not m.is_glitch_counter]

    @property
    def completed(self) -> List[Genesis1Mission]:
        """Completed real missions. Glitch counters are excluded: they also flip
        to complete (at 30 glitches in their biome), which would otherwise make
        the completed count exceed the mission count."""
        return [m for m in self.real_missions if m.complete]

    @property
    def glitch_counters(self) -> Dict[str, int]:
        """Biome -> number of glitches collected there."""
        return {m.biome or m.name: (m.glitches_collected or 0)
                for m in self.missions.values() if m.is_glitch_counter}

    @property
    def maxed_glitch_biomes(self) -> List[str]:
        """Biomes whose glitch counter reports every glitch found."""
        return [m.biome or m.name for m in self.missions.values()
                if m.is_glitch_counter and m.complete]

    @property
    def total_glitches(self) -> int:
        return sum(self.glitch_counters.values())

    @property
    def has_active_mission(self) -> bool:
        return self.active_mission_index >= 0

    def by_category(self, category: str) -> List[Genesis1Mission]:
        return [m for m in self.missions.values() if m.category == category]

    def get(self, tag: str) -> Optional[Genesis1Mission]:
        return self.missions.get(tag)

    def __len__(self):
        return len(self.missions)

    def __str__(self):
        return (f"Genesis1Missions({len(self.completed)}/{len(self.real_missions)} complete, "
                f"{self.total_glitches} glitches, active={self.active_mission_index})")

    def to_json_obj(self):
        return { "ActiveMissionIndex": self.active_mission_index,
                 "MissionData": [m.to_json_obj() for m in self.missions.values()],
                 "GlitchCounters": self.glitch_counters }

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)
