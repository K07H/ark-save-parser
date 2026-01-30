from enum import Enum
from typing import Optional

from arkparse.parsing.struct.ark_color import ArkColor
from arkparse.parsing.struct.ark_linear_color import ArkLinearColor
from arkparse.parsing.struct.ark_quat import ArkQuat
from arkparse.parsing.struct.ark_rotator import ArkRotator
from arkparse.parsing.struct.ark_tribe_rank_group import ArkTribeRankGroup

from .ark_vector import ArkVector
from .ark_unique_net_id_repl import ArkUniqueNetIdRepl
from .ark_vector_bool_pair import ArkVectorBoolPair
from .ark_tracked_actor_id_category_pair_with_bool import ArkTrackedActorIdCategoryPairWithBool
from .ark_my_persistent_buff_datas import ArkMyPersistentBuffDatas
from .ark_item_net_id import ArkItemNetId
from .ark_dino_ancestor_entry import ArkDinoAncestorEntry

class ArkStructType(Enum):
    LinearColor = "LinearColor"
    Quat = "Quat"
    Vector = "Vector"
    Rotator = "Rotator"
    UniqueNetIdRepl = "UniqueNetIdRepl"
    Color = "Color"
    VectorBoolPair = "VectorBoolPair"
    ArkTrackedActorIdCategoryPairWithBool = "TrackedActorIDCategoryPairWithBool"
    MyPersistentBuffDatas = "MyPersistentBuffDatas"
    ItemNetId = "ItemNetID"
    ArkDinoAncestor = "DinoAncestorsEntry"
    ArkTribeRankGroup = "TribeRankGroup"


    # Static constructor mapping for ArkStructType
    

    def __new__(cls, type_name: str):
        # Create a new Enum member
        obj = object.__new__(cls)
        obj._value_ = type_name
        obj.type_name = type_name
        return obj

    def __init__(self, type_name: str):
        # Access `_constructors` via the class name directly
        _constructors = {
            "LinearColor": lambda data: ArkLinearColor(data),
            "Quat": lambda data: ArkQuat(data),
            "Vector": lambda data: ArkVector(data),
            "Rotator": lambda data: ArkRotator(data),
            "UniqueNetIdRepl": lambda data: ArkUniqueNetIdRepl(data),
            "Color": lambda data: ArkColor(data),
            "VectorBoolPair": lambda data: ArkVectorBoolPair(data),
            "ArkTrackedActorIdCategoryPairWithBool": lambda data: ArkTrackedActorIdCategoryPairWithBool(data),
            "MyPersistentBuffDatas": lambda data: ArkMyPersistentBuffDatas(data),
            "ItemNetID": lambda data: ArkItemNetId(data),
            "DinoAncestorsEntry": lambda data: ArkDinoAncestorEntry(data),
            "TribeRankGroup": lambda data: ArkTribeRankGroup(data),
        }
        self.constructor = _constructors.get(type_name)

    @classmethod
    def from_type_name(cls, type_name: str) -> Optional['ArkStructType']:
        """Retrieve the ArkStructType by its type name."""
        return cls._value2member_map_.get(type_name)
    
    def to_dict(self):
        return {
            "type_name": self.type_name,
            "constructor": str(self.constructor),  # or the details you want from the constructor
        }