from dataclasses import dataclass
from uuid import UUID
from typing import TYPE_CHECKING
from arkparse.logging import ArkSaveLogger

if TYPE_CHECKING:
    from arkparse.parsing import ArkBinaryParser

@dataclass
class ObjectReference:
    TYPE_UUID = 0
    TYPE_PATH = 1
    TYPE_PATH_NO_TYPE = 2
    TYPE_NAME = 3
    TYPE_ID = 4
    TYPE_POS_MOD_REF = 5
    TYPE_NAME_2 = 256
    TYPE_UNKNOWN = -1

    type: int
    value: any

    def __init__(self, reader: "ArkBinaryParser" = None):
        if reader is None:
            self.value = None
            return
        
        reader.set_position(reader.position - 5)
        data_size = reader.read_uint32()
        reader.skip_bytes(1)  # Skip the byte we backed up for size reading

        # If the save context has a name table, handle accordingly
        if reader.save_context.has_name_table() and not reader.in_cryopod:
            ArkSaveLogger.parser_log(f"Reading type at position {reader.position} with name table")
            type = reader.read_short()
            ArkSaveLogger.parser_log(f"ObjectReference type: {type}, position: {reader.position}")

            if type == ObjectReference.TYPE_PATH or type == ObjectReference.TYPE_NAME_2:
                self.type = ObjectReference.TYPE_PATH
                self.value = reader.read_name()
            elif type == ObjectReference.TYPE_UUID:
                self.type = ObjectReference.TYPE_UUID
                self.value = reader.read_uuid_as_string()
            elif type == ObjectReference.TYPE_ID:
                self.type = ObjectReference.TYPE_ID
                self.value = reader.read_int()
            else:
                raise ValueError(f"Unknown ObjectReference type: {type}")
            return

        ArkSaveLogger.parser_log(f"Reading ObjectReference without name table at position {reader.position}")
        # Handle object types
        object_type = reader.read_int()
        if object_type == -1:
            self.type = ObjectReference.TYPE_UNKNOWN
            self.value = None
            # raise ValueError("Unknown object type encountered in ObjectReference")
        elif object_type == 0:
            self.type = ObjectReference.TYPE_ID
            self.value = reader.read_int()
        elif object_type == 1:
            self.type = ObjectReference.TYPE_PATH
            if reader.peek_name() == "ItemArchetype" and data_size == 4:
                self.value = "NONE"  # Not sure why...
                # input("DEBUG: Read NONE path object reference")
            else:
                self.value = reader.read_string()

        else:
            reader.skip_bytes(-4)
            self.type = ObjectReference.TYPE_PATH_NO_TYPE
            self.value = reader.read_string()

    def to_json_obj(self):
        obj_ref_type = self.type.__str__()
        if self.type == ObjectReference.TYPE_UUID:
            obj_ref_type = "UUID"
        if self.type == ObjectReference.TYPE_PATH:
            obj_ref_type = "PATH"
        if self.type == ObjectReference.TYPE_PATH_NO_TYPE:
            obj_ref_type = "PATH_NO_TYPE"
        if self.type == ObjectReference.TYPE_NAME:
            obj_ref_type = "NAME"
        if self.type == ObjectReference.TYPE_ID:
            obj_ref_type = "ID"
        if self.type == ObjectReference.TYPE_POS_MOD_REF:
            obj_ref_type = "POS_MOD_REF"
        if self.type == ObjectReference.TYPE_UNKNOWN:
            obj_ref_type = "UNKNOWN"
        return { "type": obj_ref_type, "value": self.value }
    
    def __str__(self):
        return f"ObjectReference(type={self.type}, value={self.value})"

def get_uuid_reference_bytes(uuid: UUID) -> bytes:
    bytes_ = bytearray()
    bytes_.extend(0x0000.to_bytes(2, byteorder="little"))
    bytes_.extend(uuid.bytes)
    return bytes_
    
