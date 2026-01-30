from ._base_value_validator import BaseValueValidator
from .struct.object_reference import ObjectReference

class PropertyParser(BaseValueValidator):
    def __init__(self, data: bytes, save_context=None):
        super().__init__(data, save_context)

    def parse_double_property(self, property_name: str) -> float:
        self.validate_name(property_name)
        self.validate_name("DoubleProperty")
        self.validate_uint32(0)
        self.validate_byte(0x08)
        self.validate_uint32(0)
        value = self.read_double()
        return value
        
    def parse_boolean_property(self, property_name: str) -> bool:
        self.validate_name(property_name)
        self.validate_name("BoolProperty")
        self.validate_uint64(0)
        value = self.peek_u16()
        if value == 1 or value == 0:
            self.read_uint16()
        else:
            value = self.read_byte()
        return value != 0

    def parse_uint32_property(self, property_name: str) -> int:
        self.validate_name(property_name)
        self.validate_name("UInt32Property")
        self.validate_uint32(0)
        self.validate_byte(0x04)
        self.validate_uint32(0)
        value = self.read_uint32()
        return value

    def parse_int32_property(self, property_name: str) -> int:
        self.validate_name(property_name)
        self.validate_name("IntProperty")
        self.validate_uint32(0)
        self.validate_byte(0x04)
        self.validate_uint32(0)
        value = self.read_int()
        return value

    def parse_byte_property(self, property_name: str) -> int:
        self.validate_string(property_name)
        self.validate_string("ByteProperty")
        present = self.read_uint32() != 1

        if present:
            is_pos = self.read_byte() == 1
            if is_pos:
                pos = self.read_uint32()
            value = self.read_byte()
            return value
        else:
            self.validate_uint32(0)
            self.validate_string("None")
            self.validate_uint16(0)
            return 0

    def parse_float_property(self, property_name: str) -> float:
        self.validate_name(property_name)
        self.validate_name("FloatProperty")
        self.validate_uint32(0)
        self.validate_byte(0x04)
        self.validate_uint32(0)
        value = self.read_float()
        return value

    def parse_string_property(self, property_name: str) -> str:
        self.validate_name(property_name)
        self.validate_name("StrProperty")
        self.validate_uint32(0)
        self.read_byte() # length?
        self.validate_uint32(0)
        value = self.read_string()
        return value
    
    def parse_name_property(self, property_name: str) -> str:
        self.validate_name(property_name)
        self.validate_name("NameProperty")
        self.validate_uint32(0)
        self.validate_byte(0x08)
        self.validate_uint32(0)
        value = self.read_name()
        return value
    
    def parse_object_reference_property(self, property_name: str) -> "ObjectReference":
        self.validate_name(property_name)
        self.validate_name("ObjectProperty")
        self.validate_uint32(0)
        self.read_uint32()
        self.validate_byte(0)
        object_reference = ObjectReference(self)
        return object_reference
    
    def parse_soft_object_property(self, property_name: str) -> str:
        self.validate_name(property_name)
        self.validate_name("SoftObjectProperty")
        self.validate_uint32(0)
        self.read_uint32()
        self.validate_byte(0)
        while(self.peek_int() != 0):
            name = self.read_name()
        self.validate_uint32(0)
        return name