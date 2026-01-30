from dataclasses import dataclass
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from ..ark_binary_parser import ArkBinaryParser

from arkparse.logging import ArkSaveLogger
from arkparse.utils.json_utils import DefaultJsonEncoder

@dataclass
class ArkTribeRankGroup:
    rank_group_name: str
    rank_group_rank: int
    inventory_rank: int
    structure_activation_rank: int
    new_structure_activation_rank: int
    new_structure_inventory_rank: int
    pet_order_rank: int
    pet_riding_rank: int
    invite_to_group_rank: int
    max_promotion_group_rank: int
    max_demotion_group_rank: int
    max_banishment_group_rank: int
    num_invites_remaining: int
    b_prevent_structure_demolish: bool
    b_prevent_structure_attachment: bool
    b_prevent_structure_build_in_range: bool
    b_prevent_unclaiming: bool
    b_allow_invites: bool
    b_limit_invites: bool
    b_allow_demotions: bool
    b_allow_promotions: bool
    b_allow_banishments: bool
    b_prevent_wireless_crafting: bool
    teleport_members_rank: int
    teleport_dinos_rank: int
    b_default_rank: bool
    b_allow_ping: bool
    b_allow_rally_point: bool

    def __init__(self, byte_buffer: "ArkBinaryParser"):
        self.rank_group_name = byte_buffer.parse_string_property("RankGroupName")
        self.rank_group_rank = byte_buffer.parse_byte_property("RankGroupRank")
        self.inventory_rank = byte_buffer.parse_byte_property("InventoryRank")
        self.structure_activation_rank = byte_buffer.parse_byte_property("StructureActivationRank")
        self.new_structure_activation_rank = byte_buffer.parse_byte_property("NewStructureActivationRank")
        self.new_structure_inventory_rank = byte_buffer.parse_byte_property("NewStructureInventoryRank")
        self.pet_order_rank = byte_buffer.parse_byte_property("PetOrderRank")
        self.pet_riding_rank = byte_buffer.parse_byte_property("PetRidingRank")
        self.invite_to_group_rank = byte_buffer.parse_byte_property("InviteToGroupRank")
        self.max_promotion_group_rank = byte_buffer.parse_byte_property("MaxPromotionGroupRank")
        self.max_demotion_group_rank = byte_buffer.parse_byte_property("MaxDemotionGroupRank")
        self.max_banishment_group_rank = byte_buffer.parse_byte_property("MaxBanishmentGroupRank")
        self.num_invites_remaining = byte_buffer.parse_byte_property("NumInvitesRemaining")
        self.b_prevent_structure_demolish = byte_buffer.parse_boolean_property("bPreventStructureDemolish")
        self.b_prevent_structure_attachment = byte_buffer.parse_boolean_property("bPreventStructureAttachment")
        self.b_prevent_structure_build_in_range = byte_buffer.parse_boolean_property("bPreventStructureBuildInRange")
        self.b_prevent_unclaiming = byte_buffer.parse_boolean_property("bPreventUnclaiming")
        self.b_allow_invites = byte_buffer.parse_boolean_property("bAllowInvites")
        self.b_limit_invites = byte_buffer.parse_boolean_property("bLimitInvites")
        self.b_allow_demotions = byte_buffer.parse_boolean_property("bAllowDemotions")
        self.b_allow_promotions = byte_buffer.parse_boolean_property("bAllowPromotions")
        self.b_allow_banishments = byte_buffer.parse_boolean_property("bAllowBanishments")
        self.b_prevent_wireless_crafting = byte_buffer.parse_boolean_property("bPreventWirelessCrafting")
        self.teleport_members_rank = byte_buffer.parse_byte_property("TeleportMembersRank")
        self.teleport_dinos_rank = byte_buffer.parse_byte_property("TeleportDinosRank")
        self.b_default_rank = byte_buffer.parse_boolean_property("bDefaultRank")
        self.b_allow_ping = byte_buffer.parse_boolean_property("bAllowPing")
        self.b_allow_rally_point = byte_buffer.parse_boolean_property("bAllowRallyPoint")

        byte_buffer.validate_string("None")

        ArkSaveLogger.parser_log(f"Read tribe rank group: {self}")

    def __str__(self) -> str:
        return f"group_name:{self.rank_group_name} group_rank:{self.rank_group_rank}"
    
    def to_json_obj(self):
        return {
            "name": self.name,
            "rank": self.rank,
            "inventory_rank": self.inventory_rank,
            "structure_activation_rank": self.structure_activation_rank,
            "new_structure_activation_rank": self.new_structure_activation_rank,
            "new_structure_inventory_rank": self.new_structure_inventory_rank,
            "pet_order_rank": self.pet_order_rank,
            "pet_riding_rank": self.pet_riding_rank,
            "invite_to_group_rank": self.invite_to_group_rank,
            "max_promotion_group_rank": self.max_promotion_group_rank,
            "max_demotion_group_rank": self.max_demotion_group_rank,
            "max_banishment_group_rank": self.max_banishment_group_rank,
            "num_invites_remaining": self.num_invites_remaining,
            "prevent_structure_demolish": self.prevent_structure_demolish,
            "prevent_structure_attachment": self.prevent_structure_attachment,
            "prevent_structure_build_in_range": self.prevent_structure_build_in_range,
            "prevent_unclaiming": self.prevent_unclaiming,
            "allow_invites": self.allow_invites,
            "limit_invites": self.limit_invites,
            "allow_demotions": self.allow_demotions,
            "allow_promotions": self.allow_promotions,
            "allow_banishments": self.allow_banishments,
            "prevent_wireless_crafting": self.prevent_wireless_crafting,
            "teleport_members_rank": self.teleport_members_rank,
            "teleport_dinos_rank": self.teleport_dinos_rank,
            "is_default_rank": self.is_default_rank,
            "allow_ping": self.allow_ping,
            "allow_rally_point": self.allow_rally_point
        }
    
    def to_json_str(self):
        return json.dumps(self.to_json_obj(), default=lambda o: o.to_json_obj() if hasattr(o, 'to_json_obj') else None, indent=4, cls=DefaultJsonEncoder)
