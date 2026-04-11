from enum import Enum

class ArkDinoTrait(Enum):
    AGGRESSIVE = "Aggressive"
    INHERIT_OXYGEN_FRAIL = "InheritOxygenFrail"
    SWIMMER = "Swimmer"
    INHERIT_WEIGHT_MUTABLE = "InheritWeightMutable"
    EXOTIC_CARRIER = "ExoticCarrier"
    INHERIT_HEALTH_ROBUST = "InheritHealthRobust"
    COWARDLY = "Cowardly"
    SCORCHED_CARRIER = "ScorchedCarrier"
    INHERIT_HEALTH_MUTABLE = "InheritHealthMutable"
    SLOW_METABOLISM = "SlowMetabolism"
    ANGRY = "Angry"
    INHERIT_MELEE_FRAIL = "InheritMeleeFrail"
    CARCASS_CARRIER = "CarcassCarrier"
    KINGSLAYING = "Kingslaying"
    INHERIT_MELEE_ROBUST = "InheritMeleeRobust"
    NOCTURNAL = "Nocturnal"
    DIURNAL = "Diurnal"
    INHERIT_HEALTH_FRAIL = "InheritHealthFrail"
    FATTY = "Fatty"
    VAMPIRIC = "Vampiric"
    MINERAL_CARRIER = "MineralCarrier"
    HEAVY_HITTING = "HeavyHitting"
    INHERIT_OXYGEN_MUTABLE = "InheritOxygenMutable"
    INHERIT_FOOD_FRAIL = "InheritFoodFrail"
    TENACIOUS = "Tenacious"
    ABERRANT_CARRIER = "AberrantCarrier"
    INHERIT_FOOD_MUTABLE = "InheritFoodMutable"
    INHERIT_OXYGEN_ROBUST = "InheritOxygenRobust"
    INHERIT_WEIGHT_ROBUST = "InheritWeightRobust"
    EXCITABLE = "Excitable"
    DISTRACTING = "Distracting"
    GIANTSLAYING = "Giantslaying"
    INHERIT_STAMINA_FRAIL = "InheritStaminaFrail"
    QUICK_HITTING = "QuickHitting"
    FRENETIC = "Frenetic"
    SPRINTER = "Sprinter"
    INHERIT_STAMINA_ROBUST = "InheritStaminaRobust"
    NUMB = "Numb"
    WARM = "Warm"
    PLANT_CARRIER = "PlantCarrier"
    INHERIT_FOOD_ROBUST = "InheritFoodRobust"
    FAST_LEARNER = "FastLearner"
    EXTINCTION_CARRIER = "ExtinctionCarrier"
    MEAT_CARRIER = "MeatCarrier"
    INHERIT_STAMINA_MUTABLE = "InheritStaminaMutable"
    PROTECTIVE = "Protective"
    INHERIT_WEIGHT_FRAIL = "InheritWeightFrail"
    ATHLETIC = "Athletic"
    COLD = "Cold"
    CAREFREE = "Carefree"
    INHERIT_MELEE_MUTABLE = "InheritMeleeMutable"
    IRONHIDE = "Ironhide"
    PACK_MULE = "PackMule"
    SHARPSHOOTER = "Sharpshooter"
    SWIFT = "Swift"
    EFFICIENT = "Efficient"
    BLOODTHIRSTY = "Bloodthirsty"
    BEASTMASTER = "Beastmaster"
    BULWARK = "Bulwark"

    def from_string(value: str) -> "ArkDinoTrait":
        if "[" in value:
            value = value[:value.index("[")]

        for trait in ArkDinoTrait:
            if trait.value == value:
                return trait
                
        raise ValueError(f"Trait {value} not found")
    
    def __str__(self):
        return self.value