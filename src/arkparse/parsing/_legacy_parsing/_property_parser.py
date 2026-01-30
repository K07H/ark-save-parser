from arkparse.parsing._base_value_validator import BaseValueValidator

class PropertyParser(BaseValueValidator):
    def __init__(self, data: bytes, save_context=None):
        super().__init__(data, save_context)

    def parse_double_property(self, property_name: str) -> float:
        self.validate_name(property_name)
        self.validate_name("DoubleProperty")
        self.validate_byte(0x08)
        self.validate_uint64(0)
        value = self.read_double()
        return value
        
    def parse_boolean_property(self, property_name: str) -> bool:
        self.validate_name(property_name)
        self.validate_name("BoolProperty")
        self.validate_uint64(0)
        value = self.read_uint16() != 0
        return value

    def parse_uint32_property(self, property_name: str) -> int:
        self.validate_name(property_name)
        self.validate_name("UInt32Property")
        self.validate_byte(0x04)
        self.validate_uint64(0)
        value = self.read_uint32()
        return value

    def parse_int32_property(self, property_name: str) -> int:
        self.validate_name(property_name)
        self.validate_name("IntProperty")
        self.validate_byte(0x04)
        self.validate_uint64(0)
        value = self.read_int()
        return value

    def parse_float_property(self, property_name: str) -> float:
        self.validate_name(property_name)
        self.validate_name("FloatProperty")
        self.validate_byte(0x04)
        self.validate_uint64(0)
        value = self.read_float()
        return value

    def parse_string_property(self, property_name: str) -> str:
        self.validate_name(property_name)
        self.validate_name("StrProperty")
        self.read_byte() # length?
        self.validate_uint64(0)
        value = self.read_string()
        return value
    
    def parse_byte_property(self, property_name: str) -> int:
        self.validate_name(property_name)
        self.validate_name("ByteProperty")
        self.read_uint32()
        self.read_uint32()
        enum_name = self.read_name()

        if enum_name == "None":
            self.read_byte()
            value = self.read_byte()
            return value
        else:
            self.read_byte()
            self.read_name()
            return 0
        