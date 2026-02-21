from typing import List, Optional
from uuid import UUID

from .ark_property_container import ArkPropertyContainer
from .ark_binary_parser import ArkBinaryParser
from arkparse.parsing.struct.ark_rotator import ArkRotator
from arkparse.parsing.struct.ark_vector import ArkVector
from arkparse.logging import ArkSaveLogger

class ArkObject(ArkPropertyContainer):
    def __init__(
        self,
        uuid: UUID,
        class_name: str,
        item: bool,
        names: List[str],
        from_data_file: bool,
        data_file_index: int,
        properties_offset: int,
        vector: Optional[ArkVector] = None,
        rotator: Optional[ArkRotator] = None
    ):
        super().__init__()
        self.uuid = uuid
        self.class_name = class_name
        self.item = item
        self.names = names
        selffrom_data_file = from_data_file
        self.data_file_index = data_file_index
        self.properties_offset = properties_offset
        self.vector = vector
        self.rotator = rotator

    @classmethod
    def from_reader(cls, reader: ArkBinaryParser, cluster_dino: bool = False) -> "ArkObject":
        uuid = reader.read_uuid()
        class_name = reader.read_string()
        item = reader.read_uint32()
        ArkSaveLogger.parser_log(f"Reading ArkObject with class {class_name} and UUID {uuid}, item={item}")
        names = reader.read_strings_array()
        ArkSaveLogger.parser_log(f"Names for object: {names}")
        from_data_file = reader.read_uint32()
        data_file_index = reader.read_int()

        vector = None
        rotator = None
        if reader.read_uint32() != 0:
            if not cluster_dino:
                vector = ArkVector(reader)
            rotator = ArkRotator(reader)
        
        ArkSaveLogger.parser_log(f"Pos: {reader.position} (hex: {hex(reader.position)})")
        properties_offset = reader.read_int()
        reader.validate_uint32(0)

        ArkSaveLogger.parser_log(f"Read ArkObject: {class_name} with UUID {uuid} at offset {properties_offset}")

        return cls(
            uuid=uuid,
            class_name=class_name,
            item=item,
            names=names,
            from_data_file=from_data_file,
            data_file_index=data_file_index,
            properties_offset=properties_offset,
            vector=vector,
            rotator=rotator
        )
    
    def __str__(self):
        return f"ArkObject(class_name={self.class_name}, uuid={self.uuid}, properties_offset={self.properties_offset})" + "\n" + super().to_string()

    def get_short_name(self) -> str:
        to_strip_end = [
            "_C",
            "_BP"
        ]

        to_strip_start = [
            "PrimalItemResource_",
            "PrimalItemAmmo_",
            "BP_"
        ]

        to_replace = {
            "_Character_BP": "",
            "_ASA_C": "",
            "StructureBP_": "",
            "PrimalItemStructure_": "",
            "PrimalItem_": "",
            "PrimalItem": "",
            "DinoCharacterStatus_BP": "Status",
        }

        short = self.class_name.split('/')[-1].split('.')[0]

        for old, new in to_replace.items():
            short = short.replace(old, new)

        for strip in to_strip_end:
            if short.endswith(strip):
                short = short[:-len(strip)]

        for strip in to_strip_start:
            if short.startswith(strip):
                short = short[len(strip):]

        return short