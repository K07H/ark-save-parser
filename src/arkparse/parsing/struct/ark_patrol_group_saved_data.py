from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:   
    from arkparse.parsing import ArkBinaryParser

class PatrolGroupProperty:
    name: str
    index: int
    uuid: str
    value: int

    def __init__(self, ark_binary_data: "ArkBinaryParser"):
        property_name = ark_binary_data.peek_name()
        value = ark_binary_data.parse_int32_property(property_name)

        parts = property_name.split("_")
        if len(parts) != 3:
            raise ValueError(f"Unexpected property name format: {property_name}")
        
        self.name = parts[0]
        self.index = int(parts[1])
        self.uuid = parts[2]
        self.value = value

    def __repr__(self):
        return f"PatrolGroupProperty(name={self.name}, index={self.index}, uuid={self.uuid}, value={self.value})"
    
    def __str__(self):
        return self.__repr__()
    
    def to_json_obj(self):
        return {
            "name": self.name,
            "index": self.index,
            "uuid": self.uuid,
            "value": self.value
        }

@dataclass
class ArkPatrolGroupSavedData:
    properties: list[PatrolGroupProperty]

    def __init__(self, ark_binary_data: "ArkBinaryParser"):
        self.properties = []

        while ark_binary_data.peek_name() != "None":
            property = PatrolGroupProperty(ark_binary_data)
            self.properties.append(property)

        ark_binary_data.validate_name("None")

    def __repr__(self):
        return f"ArkPatrolGroupSavedData(properties={self.properties})"
    
    def __str__(self):
        return self.__repr__()
    
    def to_json_obj(self):
        return {
            "properties": [prop.to_json_obj() for prop in self.properties]
        }
