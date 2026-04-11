from pathlib import Path

from arkparse.saves.asa_save import AsaSave
from arkparse.ftp.ark_ftp_client import ArkFtpClient, ArkMap
from arkparse.classes import Classes

def categorize(path: Path):
    current_dir = Path.cwd()
    new_folder = current_dir / "uncategorized"

    # Ensure the new_folder exists
    new_folder.mkdir(parents=True, exist_ok=True)

    # Load the save file
    save = AsaSave(path)
    classes = save.get_all_present_classes()

    # Define category patterns
    category_patterns = {
        "dyes": lambda cls: "Dyes" in cls,
        "structures": lambda cls: ("/Structures" in cls and "PrimalItemStructure_" not in cls) or "StructureTurretBaseBP" in cls,
        "consumables": lambda cls: "Consumables" in cls,
        "weapons": lambda cls: "Weapons" in cls and "PrimalItemAmmo" not in cls,
        "ammo": lambda cls: "Ammo" in cls,
        "armor": lambda cls: "Armor" in cls,
        "skins": lambda cls: "PrimalItemSkin" in cls,
        "dino_state": lambda cls: "DinoCharacterStatusComponent" in cls,
        "dinos": lambda cls: "Dinos/" in cls and "_Character_" in cls,
        "dino_inventories": lambda cls: "DinoTamedInventoryComponent" in cls,
        "structure_items": lambda cls: "CoreBlueprints/Items/Structures" in cls,
        "resources": lambda cls: "Resources/PrimalItemResource" in cls,
    }

    # Initialize categories with empty lists
    categorized = {category: [] for category in category_patterns}
    categorized["unknown_classes"] = []

    # Categorize classes
    for cls in classes:
        for category, match_func in category_patterns.items():
            if match_func(cls):
                categorized[category].append(cls)
                break
        else:
            categorized["unknown_classes"].append(cls)

    # Include all classes in 'all_classes.txt'
    categorized["all_classes.txt"] = classes

    # Function to filter out known classes
    def filter_new_classes(class_list):
        return [cls for cls in class_list if cls not in Classes.all_bps]

    # Apply filtering
    filtered_categorized = {file: filter_new_classes(cls_list) for file, cls_list in categorized.items()}

    # Prepare mapping of filenames to data
    file_data_mapping = {
        "all_classes.txt": filtered_categorized.get("all_classes.txt", []),
        "dyes.txt": filtered_categorized.get("dyes", []),
        "structures.txt": filtered_categorized.get("structures", []),
        "consumables.txt": filtered_categorized.get("consumables", []),
        "weapons.txt": filtered_categorized.get("weapons", []),
        "ammo.txt": filtered_categorized.get("ammo", []),
        "armor.txt": filtered_categorized.get("armor", []),
        "skins.txt": filtered_categorized.get("skins", []),
        "unknown_classes.txt": filtered_categorized.get("unknown_classes", []),
        "dino_state.txt": filtered_categorized.get("dino_state", []),
        "dinos.txt": filtered_categorized.get("dinos", []),
        "dino_inventories.txt": filtered_categorized.get("dino_inventories", []),
        "structure_items.txt": filtered_categorized.get("structure_items", []),
        "resources.txt": filtered_categorized.get("resources", []),
    }

    # Write the new classes to the new_folder without overwriting
    for filename, classes_to_write in file_data_mapping.items():
        file_path = new_folder / filename
        if not classes_to_write:
            if file_path.exists():
                file_path.unlink()  # Remove the file if no classes to write
                print(f"Removed {file_path.relative_to(current_dir)} as there are no classes for it")
            continue

        existing_classes = set()
        if file_path.exists():
            existing_classes = set(file_path.read_text().splitlines())
            # Remove known classes
            original_count = len(existing_classes)
            existing_classes -= set(Classes.all_bps)
            removed_count = original_count - len(existing_classes)
            print(f"Removed {removed_count} classes from {file_path.relative_to(current_dir)}")

        new_classes = set(classes_to_write) - existing_classes
        updated_classes = sorted(existing_classes | new_classes)

        if updated_classes:
            file_path.write_text("\n".join(updated_classes))
            print(f"Updated {file_path.relative_to(current_dir)} with {len(new_classes)} new classes")
        else:
            print(f"No new classes to add to {file_path.relative_to(current_dir)}")

# Define paths using pathlib for better readability and cross-platform support


maps = [
    # ArkMap.ABERRATION,
    # ArkMap.EXTINCTION,
    ArkMap.RAGNAROK,
    # ArkMap.SCORCHED_EARTH,
    # ArkMap.THE_CENTER,
    # ArkMap.THE_ISLAND,
    # ArkMap.ASTRAEOS
]


# base_path = Path("D:\\SteamLibrary\\steamapps\\common\\ARK Survival Ascended\\ShooterGame\\Saved\\SavedArksLocal")

# for map_name in maps:
#     categorize(base_path / f"{map_name.to_file_name()}_WP" / f"{map_name.to_file_name()}_WP.ark")

# save_path = ArkFtpClient.from_config(Path("../../ftp_config.json"), ArkMap.LOST_COLONY).download_save_file(Path.cwd())
save_path = Path.cwd() / "LostColony_WP.ark"
categorize(save_path)
