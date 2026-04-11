from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arkparse.parsing import ArkBinaryParser

LAST_NAME = None

@dataclass
class ArkMilestoneTreeLevelAndIndex:
    name: str
    level: int
    index: int

    def __init__(self, byte_buffer: "ArkBinaryParser"):
        self.name = byte_buffer.parse_name_property("Name")

        # Struct data for level and index
        self.level, self.index = self._read_level_and_index_struct(byte_buffer)

    def _read_level_and_index_struct(self, byte_buffer: "ArkBinaryParser"):
        byte_buffer.validate_name("LevelAndIndex")
        byte_buffer.validate_name("StructProperty")
        byte_buffer.validate_uint32(1)
        byte_buffer.validate_name("IntPoint")
        byte_buffer.validate_uint32(1)
        byte_buffer.validate_name("/Script/CoreUObject")
        byte_buffer.validate_uint32(0)
        byte_buffer.validate_uint32(0x08)
        level = byte_buffer.read_int()
        byte_buffer.validate_byte(0)
        index = byte_buffer.read_int()
        byte_buffer.validate_name("None")
        return level, index
    
    def to_json_obj(self):
        return {
            "name": self.name,
            "level": self.level,
            "index": self.index
        }
    
    def __str__(self):
        return f"MilestoneTreeLevelAndIndex(Name: {self.name}, Level: {self.level}, Index: {self.index})"
