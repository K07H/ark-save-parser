




from ._byte_operator import ByteOperator
from arkparse.logging import ArkSaveLogger

class BaseValueValidator(ByteOperator):
    def __init__(self, data: bytes, save_context=None):
        super().__init__(data, save_context)

    def validate_string(self, s):
        pos = self.position
        read = self.read_string()
        if read != s:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {s} but got {read} at position {pos}")
        
    def validate_uint64(self, u64):
        pos = self.position
        read = self.read_uint64()
        if read != u64:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {hex(u64)} but got {hex(read)} at position {pos}")

    def validate_uint16(self, u16):
        pos = self.position
        read = self.read_uint16()
        if read != u16:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {hex(u16)} but got {hex(read)} at position {pos}")

    def validate_uint32(self, u32):
        pos = self.position
        read = self.read_uint32()
        if read != u32:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {hex(u32)} but got {hex(read)} at position {pos}")

    def validate_byte(self, b):
        pos = self.position
        read = self.read_byte()
        if read != b:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {b} but got {read} at position {pos}")

    def validate_name(self, s):
        pos = self.position
        read = self.read_name()
        if read != s:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {s} but got {read} at position {pos}")

    def validate_int32(self, i32):
        pos = self.position
        read = self.read_int()
        if read != i32:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {hex(i32)} but got {hex(read)} at position {pos}")

    def validate_bytes_as_string(self, s, nr_bytes):
        pos = self.position
        read = self.read_bytes_as_hex(nr_bytes)
        if read != s:
            ArkSaveLogger.open_hex_view()
            raise Exception(f"Expected {s} but got {read} at position {pos}")