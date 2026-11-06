from enum import Enum


class AscensionSlot(Enum):
    """Index into the profile's 'AscensionData' array.

    The array is unlabelled, so these were established by correlating each slot
    against the *named* NumAscensions* properties on the player pawn, pooled
    over every save on disk that keeps profiles (201 profiles carrying the
    array, 107 pairable with a pawn). Every member below matched on all 107
    pairs on a non-zero value.

    Slots 0, 1, 2 and 8 are deliberately absent: see UNIDENTIFIED_SLOTS.
    """

    SCORCHED_EARTH = 3
    THE_ISLAND = 4
    ABERRATION = 5
    EXTINCTION = 6
    GENESIS = 7
    LOST_COLONY = 9

    @property
    def pawn_property(self) -> str:
        """Name of the equivalent property on the player pawn in the .ark."""
        return _PAWN_PROPERTIES[self]

    @property
    def attribute(self) -> str:
        """Name AscensionData exposes this slot under."""
        return self.name.lower()


# Slots with no identified meaning.
#
# 0-2 are three mutually independent 0-3 levels with no pawn counterpart. The
# data rules out the obvious guesses: 98 profiles have them set while the Island
# slot is 0 (so they are not a prerequisite of Island ascension) and 11 have
# Island set with one of them at 0 (so it does not imply them either).
#
# 8 was 0 for every player in every save examined, so its agreement with
# NumAscensionsGen2 is vacuous - consistent with Genesis 2, but unproven.
UNIDENTIFIED_SLOTS = (0, 1, 2, 8)

_PAWN_PROPERTIES = {
    AscensionSlot.SCORCHED_EARTH: "NumAscensionsScorched",
    AscensionSlot.THE_ISLAND: "NumAscensions",
    AscensionSlot.ABERRATION: "NumAscensionsAb",
    AscensionSlot.EXTINCTION: "NumAscensionsExt",
    AscensionSlot.GENESIS: "NumAscensionsGenesis",
    AscensionSlot.LOST_COLONY: "NumAscensionsLostColony",
}


class AscensionLevel(Enum):
    """Value held in an ascension slot."""

    NONE = 0
    GAMMA = 1
    BETA = 2
    ALPHA = 3
