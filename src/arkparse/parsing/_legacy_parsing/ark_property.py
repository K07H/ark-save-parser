from typing import Optional, TypeVar, Any
from dataclasses import dataclass, field

from arkparse.logging import ArkSaveLogger


from .struct.ark_vector import ArkVector
from .struct.ark_unique_net_id_repl import ArkUniqueNetIdRepl
from .struct.ark_vector_bool_pair import ArkVectorBoolPair
from .struct.ark_tracked_actor_id_category_pair_with_bool import ArkTrackedActorIdCategoryPairWithBool
from .struct.ark_my_persistent_buff_datas import ArkMyPersistentBuffDatas
from .struct.ark_item_net_id import ArkItemNetId
from .struct.ark_struct_type import ArkStructType
from .struct.ark_dino_ancestor_entry import ArkDinoAncestorEntry

from .ark_binary_parser import ArkBinaryParser
from arkparse.parsing.ark_value_type import ArkValueType
from arkparse.enums.ark_enum import ArkEnumValue
from arkparse.parsing.ark_property_container import ArkPropertyContainer
from arkparse.parsing.struct.ark_color import ArkColor
from arkparse.parsing.struct.ark_linear_color import ArkLinearColor
from arkparse.parsing.struct.ark_quat import ArkQuat
from arkparse.parsing.struct.ark_rotator import ArkRotator
from arkparse.parsing.struct.object_reference import ObjectReference
from arkparse.parsing.struct.ark_tribe_rank_group import ArkTribeRankGroup
from arkparse.parsing.ark_set import ArkSet

T = TypeVar('T')

@dataclass
class ArkProperty:
    name: str
    type: str
    value: Any
    position: int = field(default=0)
    unknown_byte: Optional[int] = field(default=None, repr=False)

    def __init__(self, name: str, type: str, position: int, unknown_byte: int, value: T):
        self.name = name
        self.type = type
        self.position = position
        self.unknown_byte = unknown_byte
        self.value = value
        self.binary_position = 0
        self.nr_of_bytes = 0

    def to_json_obj(self):
        return { "name": self.name, "type": self.type, "value": self.value.__str__() }

    @staticmethod
    def read_property(byte_buffer: 'ArkBinaryParser', in_array: bool = False) -> Optional['ArkProperty']:
        key = byte_buffer.read_name()

        if (key is None or key == "None") :
            ArkSaveLogger.parser_log("Exiting struct (None marker)")
            ArkSaveLogger.exit_struct()
            return None

        value_type = byte_buffer.read_value_type_by_name()
        data_size = byte_buffer.read_int()
        position = byte_buffer.read_int()
        
        start_data_position = byte_buffer.get_position()

        # print(f"Reading property {key} with type {value_type} at position {start_data_position}")
        p = None

        if(value_type != ArkValueType.Struct and value_type != ArkValueType.Array and value_type != ArkValueType.Map and value_type != ArkValueType.Set):
            pass
        else:
            ArkSaveLogger.parser_log(f"[prop={key};  type={value_type}; bin_pos={start_data_position}; size={data_size}; index_pos={position}]")

        if value_type == ArkValueType.Boolean:
            p = ArkProperty(key, value_type.name, position, 0, ArkProperty.read_property_value(value_type, byte_buffer))
            if not in_array:
                byte_buffer.validate_byte(0)
        elif value_type in {ArkValueType.Float, ArkValueType.Int, ArkValueType.Int8, ArkValueType.Double, ArkValueType.UInt32,
                            ArkValueType.UInt64, ArkValueType.UInt16, ArkValueType.Int16, ArkValueType.Int64,
                            ArkValueType.String, ArkValueType.Name, ArkValueType.SoftObject, ArkValueType.Object}:
            p = ArkProperty(key, value_type.name, position, byte_buffer.read_byte(), ArkProperty.read_property_value(value_type, byte_buffer))
        elif value_type == ArkValueType.Byte:
            pre_read_pos = byte_buffer.get_position()
            enum_type = byte_buffer.read_name()
            if enum_type == "None":
                p = ArkProperty(key, value_type.name, position, byte_buffer.read_byte(), byte_buffer.read_unsigned_byte())
            else:
                unkn_byte = byte_buffer.read_byte()
                enum_name = byte_buffer.read_name()
                ArkSaveLogger.parser_log(f"[ENUM: key={key}; value={ArkEnumValue(enum_name)}; start_pos={pre_read_pos}")
                p = ArkProperty(key, ArkValueType.Enum, position, unkn_byte, ArkEnumValue(enum_name))
        elif value_type == ArkValueType.Struct:
            struct_type = byte_buffer.read_name()
            p = ArkProperty(key, value_type.name, position, byte_buffer.read_byte(), ArkProperty.read_struct_property(byte_buffer, data_size, struct_type, in_array))
        elif value_type == ArkValueType.Array:
            p = ArkProperty.read_array_property(key, value_type.name, position, byte_buffer, data_size)
        elif value_type == ArkValueType.Map:
            p = ArkProperty.read_map_property(key, value_type.name, position, byte_buffer, data_size)
        elif value_type == ArkValueType.Set:
            p = ArkProperty.read_set_property(key, value_type.name, position, byte_buffer, data_size)
        else:
            print(f"Unsupported property type {value_type} with data size {data_size} at position {start_data_position}")
            # raise RuntimeError(f"Unsupported property type {value_type} with data size {data_size} at position {start_data_position}")
        
        if(value_type != ArkValueType.Struct and value_type != ArkValueType.Array and value_type != ArkValueType.Map and value_type != ArkValueType.Set):
            ArkSaveLogger.parser_log(f"[property read: key={key}; type={value_type}; bin_pos={start_data_position}; bin_size={data_size}; value={p.value}; index_pos={position}]")

        if p is not None:
            p.binary_position = start_data_position
            p.nr_of_bytes = data_size

        return p
    

    @staticmethod
    def read_map_property(key: str, value_type_name: str, position: int, byte_buffer: 'ArkBinaryParser', data_size: int) -> 'ArkProperty':
        key_type = byte_buffer.read_value_type_by_name()
        value_type = byte_buffer.read_value_type_by_name()

        unknown_byte = byte_buffer.read_byte()
        start_of_data = byte_buffer.get_position()
        byte_buffer.validate_uint32(0)
        count = byte_buffer.read_int()

        map_entries = []
        for _ in range(count):
            if value_type == ArkValueType.Struct:
                map_entries.append(ArkProperty.read_struct_map(key_type, byte_buffer))
            else:
                ArkSaveLogger.open_hex_view()
                raise ValueError(f"Unsupported map value type {value_type}")

        if byte_buffer.get_position() != start_of_data + data_size:
            remaining_data = byte_buffer.read_bytes(start_of_data + data_size - byte_buffer.get_position())
            ArkSaveLogger.open_hex_view()
            print("Map read incorrectly, bytes left to read:", remaining_data)
            raise ValueError("Map read incorrectly, bytes left to read")
        
        p = ArkProperty(key, value_type_name, position, unknown_byte, ArkPropertyContainer(map_entries))

        return p

    @staticmethod
    def read_struct_map(key_type: 'ArkValueType', byte_buffer: 'ArkBinaryParser') -> 'ArkProperty':
        property_values = []
        key_name = ArkProperty.read_property_value(key_type, byte_buffer)
        ArkSaveLogger.enter_struct(f"Map({key_name})")

        while byte_buffer.has_more():
            property = ArkProperty.read_property(byte_buffer)
            if property is None:
                break
            property_values.append(property)

        p = ArkProperty(key_name, "MapProperty", 0, 0, ArkPropertyContainer(property_values))
    
        ArkSaveLogger.exit_struct()

        return p

    @staticmethod
    def read_set_property(key: str, value_type_name: str, position: int, byte_buffer: 'ArkBinaryParser', data_size: int) -> 'ArkProperty':
        value_type = byte_buffer.read_value_type_by_name()
        unknown_byte = byte_buffer.read_byte()
        start_of_data = byte_buffer.get_position()
        byte_buffer.validate_uint32(0)
        count = byte_buffer.read_int()

        ArkSaveLogger.enter_struct(f"Set({value_type})")
        values = [ArkProperty.read_property_value(value_type, byte_buffer) for _ in range(count)]

        if start_of_data + data_size != byte_buffer.get_position():
            print("Set read incorrectly, bytes left to read")

        ArkSaveLogger.parser_log(f"Read set property {key} with {count} values of type {value_type_name}")
        ArkSaveLogger.parser_log(f"Set values: {values}")
        p = ArkProperty(key, value_type_name, position, unknown_byte, ArkSet(value_type, values))

        ArkSaveLogger.exit_struct()

        return p

    @staticmethod
    def read_soft_object_property_value(byte_buffer: 'ArkBinaryParser') -> str:
        ArkSaveLogger.enter_struct("SfO")
        names = []
        while byte_buffer.peek_int() != 0:
            obj_name = byte_buffer.read_name()
            names.append(obj_name)
        byte_buffer.validate_bytes_as_string("00 00 00 00", 4)
        ArkSaveLogger.parser_log(f"Read soft object property {names}")
        ArkSaveLogger.exit_struct()
        return names

    @staticmethod
    def read_struct_property(byte_buffer: 'ArkBinaryParser', data_size: int, struct_type: str, in_array: bool) -> Any:       
        ArkSaveLogger.parser_log(f"Reading struct property {struct_type} with data size {data_size}")
        if not in_array:
            ArkSaveLogger.enter_struct(f"S({struct_type})")
            byte_buffer.validate_bytes_as_string("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00", 16)

        ark_struct_type = ArkStructType.from_type_name(struct_type)
        
        # print("Struct type:", ark_struct_type)
        if ark_struct_type or in_array:
            p = None
            if ark_struct_type == ArkStructType.Color:
                p = ArkColor(byte_buffer)
            elif ark_struct_type == ArkStructType.LinearColor:
                p = ArkLinearColor(byte_buffer)
            elif ark_struct_type == ArkStructType.Quat:
                p = ArkQuat(byte_buffer)
            elif ark_struct_type == ArkStructType.Rotator:
                p = ArkRotator(byte_buffer)
            elif ark_struct_type == ArkStructType.Vector:
                p = ArkVector(byte_buffer)
            elif ark_struct_type == ArkStructType.UniqueNetIdRepl:
                p = ArkUniqueNetIdRepl(byte_buffer)
            elif ark_struct_type == ArkStructType.VectorBoolPair:
                p = ArkVectorBoolPair(byte_buffer)
            elif ark_struct_type == ArkStructType.ArkTrackedActorIdCategoryPairWithBool:
                p = ArkTrackedActorIdCategoryPairWithBool(byte_buffer)
            elif ark_struct_type == ArkStructType.MyPersistentBuffDatas:
                p = ArkMyPersistentBuffDatas(byte_buffer, data_size)
            elif ark_struct_type == ArkStructType.ItemNetId:
                p = ArkItemNetId(byte_buffer)
            elif ark_struct_type == ArkStructType.ArkDinoAncestor:
                p = ArkDinoAncestorEntry(byte_buffer)
            elif ark_struct_type == ArkStructType.ArkTribeRankGroup:
                p = ArkTribeRankGroup(byte_buffer)
            elif ark_struct_type == None:
                return None
            elif in_array:
                if byte_buffer.peek_name() == "None":
                    return byte_buffer.read_name()
                else:
                    ArkSaveLogger.enable_debug = True
                    ArkSaveLogger.open_hex_view(True)
                    raise ValueError(f"Unsupported struct type {ark_struct_type}")
            
            if not in_array:
                ArkSaveLogger.exit_struct()
            return p

        position = byte_buffer.get_position()
        properties = ArkProperty.read_struct_properties(byte_buffer)

        if byte_buffer.get_position() != position + data_size and not in_array:
            ArkSaveLogger.warning_log("Struct reading position mismatch for type", struct_type)
            ArkSaveLogger.warning_log(f"StructType: {struct_type}, DataSize: {data_size}, Position: {position}, CurrentPosition: {byte_buffer.get_position()}")
            byte_buffer.set_position(position + data_size)
            # ArkSaveLogger.open_hex_view()
            # raise Exception("Struct reading position mismatch: [StructType: %s, DataSize: %d, Position: %d, CurrentPosition: %d]" % (struct_type, data_size, position, byte_buffer.get_position()))
        
        # ArkSaveLogger.exit_struct()
        return properties

    @staticmethod
    def read_struct_properties(byte_buffer: 'ArkBinaryParser') -> 'ArkPropertyContainer':
        properties = []
        
        struct_property = ArkProperty.read_property(byte_buffer)
        ArkSaveLogger.parser_log(f"Struct properties: {struct_property.name} {struct_property.type} {struct_property.value}")
        while struct_property:
            properties.append(struct_property)
            if byte_buffer.has_more():
                struct_property = ArkProperty.read_property(byte_buffer)
                if struct_property is not None:
                    ArkSaveLogger.parser_log(f"Struct properties: {struct_property.name} {struct_property.type} {struct_property.value}")
            else:
                break
        
        ArkSaveLogger.parser_log(f"Read {len(properties)} struct properties")
        return ArkPropertyContainer(properties)

    @staticmethod
    def read_array_property(key: str, type_: str, position: int, byte_buffer: 'ArkBinaryParser', data_size: int) -> 'ArkProperty':
        array_type = byte_buffer.read_name()
        end_of_struct = byte_buffer.read_byte()
        data_start_postion = byte_buffer.get_position()
        array_length = byte_buffer.read_int()
        start_of_array_values_position = byte_buffer.get_position()

        if array_type == "StructProperty":
            array_name = byte_buffer.read_name()
            sProp = byte_buffer.read_name()

            if sProp != "StructProperty":
                ArkSaveLogger.open_hex_view()
                raise ValueError(f"Expected StructProperty, got {sProp}")
            
            content_size = byte_buffer.read_uint64()
            array_content_type = byte_buffer.read_name()
            byte_buffer.skip_bytes(17)
            ArkSaveLogger.enter_struct(f"Arr({array_content_type})")
            ArkSaveLogger.parser_log(f"[STRUCT ARRAY: key=\'{array_name}\'; nr_of_value={array_length}; type={array_content_type}; bin_length={content_size}]")
            struct_array = []
            for _ in range(array_length):
                struct_array.append(ArkProperty.read_struct_property(byte_buffer, content_size, array_content_type, True))

            if array_content_type == "CustomItemByteArray":
                struct_array = []
                for _ in range(array_length):
                    struct_array.append(ArkProperty.read_property(byte_buffer))
                    none = ArkProperty.read_property(byte_buffer)
                    ArkSaveLogger.enter_struct("Arr(CustomItemByteArray)")
                    if none is not None:
                        raise ValueError(f"Expected None, got {none}")
                    
                    dinostate = struct_array[0].value
                    # if len(dinostate) > 0:
                    #     bytes_ = bytes(dinostate)
                    #     print(f"Bytes: {bytes_}")
                    #     newReader = ArkBinaryParser(bytes_, byte_buffer.save_context)
                    #     ArkSaveLogger.set_file(newReader, "debug.bin")
                    #     newReader.find_names()
                    #     ArkSaveLogger.open_hex_view(True)

            p = ArkProperty(key, type_, position, end_of_struct, struct_array)

            ArkSaveLogger.parser_log(f"============ END {array_name}[{array_content_type}] ============")

            if(byte_buffer.position != data_start_postion + data_size):
                # just skip to the end of the struct if an error occurs
                byte_buffer.set_position(data_start_postion + data_size)
                # byte_buffer.find_names()
                # ArkSaveLogger.open_hex_view()
                # raise ValueError(f"Array read incorrectly, bytes left to read: {data_start_postion + data_size - byte_buffer.position}")
            
            ArkSaveLogger.exit_struct()
            return p
    
        else:
            ArkSaveLogger.enter_struct(f"Arr({array_type})")
            ArkSaveLogger.parser_log(f"[VALUE ARRAY: key={key}; nr_of_values={array_length}; type={array_type}]")

            if key == "MyPersistentBuffDatas":
                p = ArkProperty(key, "Struct", position, 0x00, ArkProperty.read_struct_property(byte_buffer, array_length, key, True))
            else:
                array = []
                for _ in range(array_length):
                    if byte_buffer.read_uint32 == 0x09AD2622:
                        array.append(byte_buffer.read_name())
                    else:
                        array.append(ArkProperty.read_property_value(ArkValueType.from_name(array_type), byte_buffer))

                if array_type != "ByteProperty":
                    for i, value in enumerate(array):
                        ArkSaveLogger.parser_log(f"value {i}: {value}")
                else:
                    ArkSaveLogger.parser_log(f"Array value: {array}")
                    
    
                p = ArkProperty(key, type_, position, end_of_struct, array)

            ArkSaveLogger.parser_log(f"============ END Arr({array_type}) ============")

            # if(byte_buffer.position != data_start_postion + data_size):
            #     ArkSaveLogger.open_hex_view()
            #     raise ValueError(f"Array read incorrectly, bytes left to read: {data_start_postion + data_size - byte_buffer.position}")
            
            ArkSaveLogger.exit_struct()
        
            return p

    @staticmethod
    def read_property_value(value_type: ArkValueType, byte_buffer: ArkBinaryParser) -> Any:
        if value_type == ArkValueType.Byte:
            return byte_buffer.read_unsigned_byte()
        elif value_type == ArkValueType.Int8:
            return byte_buffer.read_byte()
        elif value_type == ArkValueType.Double:
            return byte_buffer.read_double()
        elif value_type == ArkValueType.Float:
            return byte_buffer.read_float()
        elif value_type == ArkValueType.Int:
            return byte_buffer.read_int()
        elif value_type == ArkValueType.Object:
            return ObjectReference(byte_buffer)
        elif value_type == ArkValueType.String:
            return byte_buffer.read_string()
        elif value_type == ArkValueType.UInt32:
            return byte_buffer.read_uint32()
        elif value_type == ArkValueType.UInt64:
            return byte_buffer.read_uint64()
        elif value_type == ArkValueType.UInt16:
            return byte_buffer.read_uint16()
        elif value_type == ArkValueType.Int16:
            return byte_buffer.read_short()
        elif value_type == ArkValueType.Int64:
            return byte_buffer.read_int64()
        elif value_type == ArkValueType.Name:
            return byte_buffer.read_name()
        elif value_type == ArkValueType.Boolean:
            return byte_buffer.read_byte() == 1
        elif value_type == ArkValueType.Struct:
            return ArkProperty.read_struct_property(byte_buffer, byte_buffer.read_int(), True)
        elif value_type == ArkValueType.SoftObject:
            return ArkProperty.read_soft_object_property_value(byte_buffer)
        else:
            raise RuntimeError(f"Cannot read value type: {value_type} at position {byte_buffer.get_position()}")
            