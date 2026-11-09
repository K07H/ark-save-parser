import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TYPE_CHECKING

from arkparse.enums import AscensionSlot, AscensionLevel, UNIDENTIFIED_SLOTS
from arkparse.logging import ArkSaveLogger
from arkparse.parsing import ArkPropertyContainer
from arkparse.utils.json_utils import DefaultJsonEncoder

if TYPE_CHECKING:
    from arkparse.object_model.ark_game_object import ArkGameObject
    from arkparse.player.ark_player import ArkPlayer


@dataclass
class AscensionData:
    """The 'AscensionData' array of a player profile.

    The array lives at the top level of PrimalPlayerDataBP_C (a sibling of
    'MyData', not inside it) and holds one float per ascension slot, valued
    0..3 for none/gamma/beta/alpha.

    It grows as maps are added, so older profiles are shorter (9 entries,
    without Lost Colony) than newer ones (10). Every read goes through get(),
    which returns 0 for a slot the array does not reach.

    Slot meanings are AscensionSlot; the slots that could not be identified are
    kept in `unidentified` rather than guessed at. A non-zero value in one of
    those, or a slot past the end of AscensionSlot, is warned about: it is the
    signal that a slot has become meaningful (a new map, most likely) and that
    the mapping needs revisiting. Slots 0-2 are set on most profiles, so each
    slot is warned about once per process rather than once per player.
    """

    # Slots already warned about, so a whole save's worth of profiles does not
    # repeat the same warning hundreds of times.
    _warned_slots = set()

    values: List[int] = field(default_factory=list)

    scorched_earth: int = 0
    the_island: int = 0
    aberration: int = 0
    extinction: int = 0
    genesis: int = 0
    lost_colony: int = 0

    unidentified: Dict[int, int] = field(default_factory=dict)

    def __init__(self, properties: Optional[ArkPropertyContainer] = None):
        raw = properties.get_array_property_value("AscensionData", []) if properties else []
        # Stored as floats, but only ever whole levels.
        self.values = [int(v) for v in raw]

        for slot in AscensionSlot:
            setattr(self, slot.attribute, self.get(slot))

        self.unidentified = {slot: self.get(slot) for slot in UNIDENTIFIED_SLOTS}
        self._warn_about_unidentified()

    @classmethod
    def from_player(cls, player: "ArkPlayer") -> "AscensionData":
        return cls(player.player_data)

    @classmethod
    def from_pawn(cls, pawn: "ArkGameObject") -> "AscensionData":
        """Build the same view from a player pawn in the .ark.

        The pawn carries the ascension levels as separately named properties
        rather than as an array, and is the only source when a profile has no
        'AscensionData' at all. The unidentified slots have no pawn equivalent
        and stay 0.
        """
        instance = cls()
        instance.values = [0] * (max(s.value for s in AscensionSlot) + 1)
        for slot in AscensionSlot:
            level = pawn.get_property_value(slot.pawn_property) or 0
            instance.values[slot.value] = level
            setattr(instance, slot.attribute, level)
        instance.unidentified = {slot: 0 for slot in UNIDENTIFIED_SLOTS}
        return instance

    def _warn_about_unidentified(self) -> None:
        for slot, level in self.unidentified.items():
            if level and slot not in self._warned_slots:
                self._warned_slots.add(slot)
                ArkSaveLogger.warning_log(
                    f"AscensionData slot {slot} is set (e.g. {level}) but has no identified "
                    f"meaning; it is kept in AscensionData.unidentified"
                )

        known = max((s.value for s in AscensionSlot), default=-1)
        for slot in range(known + 1, len(self.values)):
            if slot in self._warned_slots:
                continue
            self._warned_slots.add(slot)
            ArkSaveLogger.warning_log(
                f"AscensionData slot {slot} is past every known slot (value {self.values[slot]}); "
                f"a new ascension slot may have been added"
            )

    @classmethod
    def reset_warnings(cls) -> None:
        """Warn again about slots already reported (for tests or a second sweep)."""
        cls._warned_slots.clear()

    def get(self, slot) -> int:
        """Level for a slot, 0 when the profile predates that slot.

        Accepts an AscensionSlot or a raw index.
        """
        index = slot.value if isinstance(slot, AscensionSlot) else slot
        return self.values[index] if 0 <= index < len(self.values) else 0

    def level(self, slot) -> AscensionLevel:
        return AscensionLevel(self.get(slot))

    @property
    def has_data(self) -> bool:
        """False for the profiles that carry no 'AscensionData' property."""
        return len(self.values) > 0

    @property
    def ascended_maps(self) -> Dict[AscensionSlot, AscensionLevel]:
        """Identified maps the player ascended on, mapped to their level."""
        return {slot: self.level(slot) for slot in AscensionSlot if self.get(slot) > 0}

    def __str__(self):
        if not self.has_data:
            return "AscensionData: (none)"
        ascended = ", ".join(f"{slot.attribute}={level.name.lower()}"
                             for slot, level in self.ascended_maps.items())
        return f"AscensionData({ascended or 'no identified ascensions'}; raw={self.values})"

    def to_json_obj(self):
        json_obj = { "AscensionData": self.values }
        for slot in AscensionSlot:
            json_obj[slot.pawn_property] = getattr(self, slot.attribute)
        json_obj["UnidentifiedSlots"] = self.unidentified
        return json_obj

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)
