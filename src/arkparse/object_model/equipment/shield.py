import json
from uuid import UUID

from arkparse import AsaSave
from arkparse.object_model.ark_game_object import ArkGameObject
from arkparse.parsing import ArkBinaryParser
from arkparse.enums import ArkEquipmentStat
from arkparse.utils.json_utils import DefaultJsonEncoder

from .__equipment_with_durability import EquipmentWithDurability

class Shield(EquipmentWithDurability):
    def __init_props__(self, obj: ArkGameObject = None):
        super().__init_props__(obj)

    def __init__(self, uuid: UUID = None, binary: ArkBinaryParser = None):
        super().__init__(uuid, binary)
        self.class_name = "shield"

    def auto_rate(self, save: AsaSave = None):
        self._auto_rate(0.000519, self.get_average_stat(), save)    

    def get_stat_for_rating(self, stat: ArkEquipmentStat, rating: float) -> float:
        value = super()._get_stat_for_rating(stat, rating, 0.000519)
        return self.get_actual_value(stat, value)

    @staticmethod
    def from_object(obj: ArkGameObject):
        shield = Shield()
        shield.__init_props__(obj)
        
        return shield

    def __str__(self):
        return f"Shield: {self.get_short_name()} - CurrentDurability: {self.current_durability} - Durability: {self.durability} - BP: {self.is_bp} - Crafted: {self.is_crafted()} - Rating: {self.rating}"

    def to_json_obj(self):
        return super().to_json_obj()

    def to_json_str(self):
        return json.dumps(self.to_json_obj(), indent=4, cls=DefaultJsonEncoder)
