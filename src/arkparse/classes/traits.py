"""Item trait blueprint paths grouped by type and rarity (Lesser/Moderate/Greater).

Structure mirrors other classes in this package: top-level type classes (`Armor`,
`Gun`, `Melee`, `Projectile`) each expose `.greater`, `.moderate`, `.lesser`
instances and an `all_bps` list combining them.
"""

class ArmorGreater:
    ammo_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_AmmoOnHit.PrimalItem_ItemTrait_Armor_AmmoOnHit_C"
    increased_incoming_healing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing.PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing_C"
    marathon: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Marathon.PrimalItem_ItemTrait_Armor_Marathon_C"
    mobile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Mobile.PrimalItem_ItemTrait_Armor_Mobile_C"
    reduced_debuff_duration: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_ReducedDebuffDuration.PrimalItem_ItemTrait_Armor_ReducedDebuffDuration_C"
    all_bps = [ammo_on_hit, increased_incoming_healing, marathon, mobile, reduced_debuff_duration]

class ArmorLesser:
    ammo_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_AmmoOnHit_Lesser.PrimalItem_ItemTrait_Armor_AmmoOnHit_Lesser_C"
    increased_incoming_healing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing_Lesser.PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing_Lesser_C"
    marathon: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Marathon_Lesser.PrimalItem_ItemTrait_Armor_Marathon_Lesser_C"
    mobile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Mobile_Lesser.PrimalItem_ItemTrait_Armor_Mobile_Lesser_C"
    reduced_debuff_duration: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_ReducedDebuffDuration_Lesser.PrimalItem_ItemTrait_Armor_ReducedDebuffDuration_Lesser_C"
    all_bps = [ammo_on_hit, increased_incoming_healing, marathon, mobile, reduced_debuff_duration]

class ArmorModerate:
    ammo_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_AmmoOnHit_Moderate.PrimalItem_ItemTrait_Armor_AmmoOnHit_Moderate_C"
    increased_incoming_healing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing_Moderate.PrimalItem_ItemTrait_Armor_IncreasedIncomingHealing_Moderate_C"
    marathon: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Marathon_Moderate.PrimalItem_ItemTrait_Armor_Marathon_Moderate_C"
    mobile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_Mobile_Moderate.PrimalItem_ItemTrait_Armor_Mobile_Moderate_C"
    reduced_debuff_duration: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Armor_ReducedDebuffDuration_Moderate.PrimalItem_ItemTrait_Armor_ReducedDebuffDuration_Moderate_C"
    all_bps = [ammo_on_hit, increased_incoming_healing, marathon, mobile, reduced_debuff_duration]

class GunGreater:
    cannibalizing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Cannibalizing.PrimalItem_ItemTrait_Gun_Cannibalizing_C"
    focusing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Focusing.PrimalItem_ItemTrait_Gun_Focusing_C"
    reduced_damage_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_ReducedDamageOnHit.PrimalItem_ItemTrait_Gun_ReducedDamageOnHit_C"
    ricochet: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Ricochet.PrimalItem_ItemTrait_Gun_Ricochet_C"
    tracker: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Tracker.PrimalItem_ItemTrait_Gun_Tracker_C"
    all_bps = [cannibalizing, focusing, reduced_damage_on_hit, ricochet, tracker]

class GunLesser:
    cannibalizing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Cannibalizing_Lesser.PrimalItem_ItemTrait_Gun_Cannibalizing_Lesser_C"
    focusing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Focusing_Lesser.PrimalItem_ItemTrait_Gun_Focusing_Lesser_C"
    reduced_damage_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_ReducedDamageOnHit_Lesser.PrimalItem_ItemTrait_Gun_ReducedDamageOnHit_Lesser_C"
    ricochet: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Ricochet_Lesser.PrimalItem_ItemTrait_Gun_Ricochet_Lesser_C"
    tracker: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Tracker_Lesser.PrimalItem_ItemTrait_Gun_Tracker_Lesser_C"
    all_bps = [cannibalizing, focusing, reduced_damage_on_hit, ricochet, tracker]

class GunModerate:
    cannibalizing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Cannibalizing_Moderate.PrimalItem_ItemTrait_Gun_Cannibalizing_Moderate_C"
    focusing: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Focusing_Moderate.PrimalItem_ItemTrait_Gun_Focusing_Moderate_C"
    reduced_damage_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_ReducedDamageOnHit_Moderate.PrimalItem_ItemTrait_Gun_ReducedDamageOnHit_Moderate_C"
    ricochet: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Ricochet_Moderate.PrimalItem_ItemTrait_Gun_Ricochet_Moderate_C"
    tracker: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Gun_Tracker_Moderate.PrimalItem_ItemTrait_Gun_Tracker_Moderate_C"
    all_bps = [cannibalizing, focusing, reduced_damage_on_hit, ricochet, tracker]

class MeleeGreater:
    heal_on_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_HealOnDamage.PrimalItem_ItemTrait_Melee_HealOnDamage_C"
    increased_damage_from_behind: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind.PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind_C"
    increased_damage_to_non_living: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving.PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving_C"
    increased_speed_and_damage_taken: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken.PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken_C"
    shield_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_ShieldOnHit.PrimalItem_ItemTrait_Melee_ShieldOnHit_C"
    all_bps = [heal_on_damage, increased_damage_from_behind, increased_damage_to_non_living, increased_speed_and_damage_taken, shield_on_hit]

class MeleeLesser:
    heal_on_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_HealOnDamage_Lesser.PrimalItem_ItemTrait_Melee_HealOnDamage_Lesser_C"
    increased_damage_from_behind: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind_Lesser.PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind_Lesser_C"
    increased_damage_to_non_living: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving_Lesser.PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving_Lesser_C"
    increased_speed_and_damage_taken: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken_Lesser.PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken_Lesser_C"
    shield_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_ShieldOnHit_Lesser.PrimalItem_ItemTrait_Melee_ShieldOnHit_Lesser_C"
    all_bps = [heal_on_damage, increased_damage_from_behind, increased_damage_to_non_living, increased_speed_and_damage_taken, shield_on_hit]

class MeleeModerate:
    heal_on_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_HealOnDamage_Moderate.PrimalItem_ItemTrait_Melee_HealOnDamage_Moderate_C"
    increased_damage_from_behind: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind_Moderate.PrimalItem_ItemTrait_Melee_IncreasedDamageFromBehind_Moderate_C"
    increased_damage_to_non_living: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving_Moderate.PrimalItem_ItemTrait_Melee_IncreasedDamageToNonLiving_Moderate_C"
    increased_speed_and_damage_taken: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken_Moderate.PrimalItem_ItemTrait_Melee_IncreasedSpeedAndDamageTaken_Moderate_C"
    shield_on_hit: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Melee_ShieldOnHit_Moderate.PrimalItem_ItemTrait_Melee_ShieldOnHit_Moderate_C"
    all_bps = [heal_on_damage, increased_damage_from_behind, increased_damage_to_non_living, increased_speed_and_damage_taken, shield_on_hit]

class ProjectileGreater:
    antigrav: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_Antigrav.PrimalItem_ItemTrait_Projectile_Antigrav_C"
    extra_damage_to_vulnerable: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable.PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable_C"
    increased_damage_to_alpha: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha.PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha_C"
    increased_first_hit_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage.PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage_C"
    second_projectile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_SecondProjectile.PrimalItem_ItemTrait_Projectile_SecondProjectile_C"
    all_bps = [antigrav, extra_damage_to_vulnerable, increased_damage_to_alpha, increased_first_hit_damage, second_projectile]

class ProjectileLesser:
    antigrav: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_Antigrav_Lesser.PrimalItem_ItemTrait_Projectile_Antigrav_Lesser_C"
    extra_damage_to_vulnerable: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable_Lesser.PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable_Lesser_C"
    increased_damage_to_alpha: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha_Lesser.PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha_Lesser_C"
    increased_first_hit_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage_Lesser.PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage_Lesser_C"
    second_projectile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_SecondProjectile_Lesser.PrimalItem_ItemTrait_Projectile_SecondProjectile_Lesser_C"
    all_bps = [antigrav, extra_damage_to_vulnerable, increased_damage_to_alpha, increased_first_hit_damage, second_projectile]

class ProjectileModerate:
    antigrav: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_Antigrav_Moderate.PrimalItem_ItemTrait_Projectile_Antigrav_Moderate_C"
    extra_damage_to_vulnerable: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable_Moderate.PrimalItem_ItemTrait_Projectile_ExtraDamageToVulnerable_Moderate_C"
    increased_damage_to_alpha: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha_Moderate.PrimalItem_ItemTrait_Projectile_IncreasedDamageToAlpha_Moderate_C"
    increased_first_hit_damage: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage_Moderate.PrimalItem_ItemTrait_Projectile_IncreasedFirstHitDamage_Moderate_C"
    second_projectile: str = "/Game/Packs/Wasteland/CoreBlueprints/ItemTraits/Items/PrimalItem_ItemTrait_Projectile_SecondProjectile_Moderate.PrimalItem_ItemTrait_Projectile_SecondProjectile_Moderate_C"
    all_bps = [antigrav, extra_damage_to_vulnerable, increased_damage_to_alpha, increased_first_hit_damage, second_projectile]

class Armor:
    greater: ArmorGreater = ArmorGreater()
    moderate: ArmorModerate = ArmorModerate()
    lesser: ArmorLesser = ArmorLesser()
    all_bps = greater.all_bps + moderate.all_bps + lesser.all_bps

class Gun:
    greater: GunGreater = GunGreater()
    moderate: GunModerate = GunModerate()
    lesser: GunLesser = GunLesser()
    all_bps = greater.all_bps + moderate.all_bps + lesser.all_bps

class Melee:
    greater: MeleeGreater = MeleeGreater()
    moderate: MeleeModerate = MeleeModerate()
    lesser: MeleeLesser = MeleeLesser()
    all_bps = greater.all_bps + moderate.all_bps + lesser.all_bps

class Projectile:
    greater: ProjectileGreater = ProjectileGreater()
    moderate: ProjectileModerate = ProjectileModerate()
    lesser: ProjectileLesser = ProjectileLesser()
    all_bps = greater.all_bps + moderate.all_bps + lesser.all_bps

class Traits:
    armor: Armor = Armor()
    gun: Gun = Gun()
    melee: Melee = Melee()
    projectile: Projectile = Projectile()
    all_bps = armor.all_bps + gun.all_bps + melee.all_bps + projectile.all_bps

