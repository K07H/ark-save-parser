import json
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from arkparse.parsing import ArkPropertyContainer
from arkparse.utils.json_utils import DefaultJsonEncoder

if TYPE_CHECKING:
    from arkparse.object_model.ark_game_object import ArkGameObject
    from arkparse.player.ark_player import ArkPlayer

# Milestone tasks that track hexagon spending (Tides of Fortune).
SPEND_HEXAGON_MILESTONES = ("Task.ToF.SpendHexagonsA", "Task.ToF.SpendHexagonsB")


@dataclass
class HexagonState:
    """A player's hexagon balance and hexagon-related milestone progress.

    The balance is stored twice:
      * 'HexagonCount' at the top level of PrimalPlayerDataBP_C (a sibling of
        'MyData', not inside it) - the profile, and the authoritative source
      * 'PlayerHexagonCount' on the player pawn inside the .ark

    Both agreed for every player that had both in the Genesis test save, but
    only the profile covers players whose pawn is not in the save, so `count`
    reads the profile and `pawn_count` is filled in only when a pawn is given.

    Players who never earned hexagons have no property at all, hence the 0
    defaults rather than None.
    """

    count: int = 0
    pawn_count: Optional[int] = None

    completed_spend_milestones: List[str] = field(default_factory=list)
    current_spend_milestones: List[str] = field(default_factory=list)

    def __init__(self, properties: Optional[ArkPropertyContainer] = None,
                 pawn: Optional["ArkGameObject"] = None):
        self.count = 0
        self.pawn_count = None
        self.completed_spend_milestones = []
        self.current_spend_milestones = []

        if properties is not None:
            self.count = properties.get_property_value("HexagonCount", 0)

            stats = properties.get_property_value("MyPersistentCharacterStats")
            if stats is not None:
                self.completed_spend_milestones = self._spend_tasks(stats, "CompletedMilestones")
                self.current_spend_milestones = self._spend_tasks(stats, "CurrentMilestones")

        if pawn is not None:
            self.pawn_count = pawn.get_property_value("PlayerHexagonCount", 0)

    @classmethod
    def from_player(cls, player: "ArkPlayer", pawn: Optional["ArkGameObject"] = None) -> "HexagonState":
        return cls(player.player_data, pawn)

    @staticmethod
    def _spend_tasks(stats: ArkPropertyContainer, name: str) -> List[str]:
        return [task for task in stats.get_array_property_value(name, [])
                if task in SPEND_HEXAGON_MILESTONES]

    @property
    def has_hexagons(self) -> bool:
        return self.count > 0

    @property
    def is_consistent(self) -> bool:
        """Whether the profile and the pawn agree. True when there is no pawn."""
        return self.pawn_count is None or self.pawn_count == self.count

    def __str__(self):
        pawn = "" if self.pawn_count is None else f" (pawn={self.pawn_count}{'' if self.is_consistent else ', MISMATCH'})"
        return f"HexagonState(count={self.count}{pawn})"

    def to_json_obj(self):
        return { "HexagonCount": self.count,
                 "PlayerHexagonCount": self.pawn_count,
                 "CompletedSpendMilestones": self.completed_spend_milestones,
                 "CurrentSpendMilestones": self.current_spend_milestones }

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)
