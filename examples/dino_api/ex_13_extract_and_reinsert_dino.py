from pathlib import Path
from arkparse import Classes
from arkparse.enums import ArkMap
from arkparse.api.dino_api import DinoApi
from arkparse.api.structure_api import StructureApi
from arkparse.saves.asa_save import AsaSave
from arkparse.object_model.dinos.tamed_dino import TamedDino

export_save_path = AsaSave(Path.cwd() / "Ragnarok_62c4f206-cd09-4c2a-b1e7-256796ee6f81.ark")                   # load the save file
export_dino_api = DinoApi(export_save_path)                             # create a DinoApi object
export_dinos = export_dino_api.get_all_tamed(include_cryopodded=True)  # Cryopods can be exported and inserted as items, not entirely the same as active dinos

my_dino: TamedDino = None
search_name = "DinoName"  # replace with the name of the dino you want to export and re-insert
tribe_id = 1510471994

for dino in export_dinos.values():
    if dino.tamed_name == search_name:
        my_dino = dino
        print(f"Found dino {dino.tamed_name} ({dino.uuid}) for export")

# target save
import_save_path  = Path.cwd() / "_Ragnarok_WP.ark"
import_save = AsaSave(import_save_path)

# get vault of target tribe in case the dino is to be inserted as cryopod
vaults = StructureApi(import_save).get_by_class([Classes.structures.placed.utility.vault])
vault = None
for v in vaults.values():
    if v.owner.tribe_id == tribe_id:
        print(f"Found vault of tribe {tribe_id} at {v.location.as_map_coords(ArkMap.RAGNAROK)}")
        vault = v
        break

if my_dino.cryopod is not None:
    # insert into vault as cryopod
    import_save.add_obj_to_db(my_dino.cryopod.uuid, my_dino.cryopod.binary.byte_buffer)
    vault.add_item(my_dino.cryopod.uuid)
    print(f"Inserted cryopod of dino {my_dino.tamed_name} ({my_dino.uuid}) into vault at {vault.location.as_map_coords(ArkMap.RAGNAROK)}")
else:
    export_path = Path.cwd() / "exports" / str(my_dino.uuid)
    my_dino.store_binary(export_path)
    import_dino_api = DinoApi(import_save)
    import_dino_api.import_dino(export_path)
    print(f"Inserted dino {my_dino.tamed_name} ({my_dino.uuid}) into save directly")

# store
import_save.store_db(Path.cwd() / "Ragnarok_WP.ark")
print(f"Inserted dino {my_dino.tamed_name} ({my_dino.uuid}) into import.ark and saved as updated.ark")

# verify
verify_save = AsaSave(Path.cwd() / "Ragnarok_WP.ark")
verify_dino_api = DinoApi(verify_save)
verify_dinos = verify_dino_api.get_all_tamed()
print("Dinos in verify save:")
for d in verify_dinos.values():
    if d.tamed_name == my_dino.tamed_name:
        print(f"Found imported dino {d.tamed_name} ({d.uuid})")
