import json
from logging import getLogger
import os
from pathlib import Path
import shutil
import subprocess

from builder.utils.env import MODS_CONFIG_FILE, SERVER_MODS_FOLDER, SERVER_MODS_KEYS_FOLDER, STEAM_PASSWORD, STEAM_USER, TMP_MODS_FOLDER

LOGGER = getLogger()
    
def copy_mods_keys() -> None:
    LOGGER.info("Reset mods keys")
    
    # reset mods keys
    for filename in os.listdir(SERVER_MODS_KEYS_FOLDER):
        file = SERVER_MODS_KEYS_FOLDER / filename
        
        if file.is_dir():
            shutil.rmtree(file)
        elif file.is_file() and filename != "a3.bikey":
            os.remove(file)
            
    LOGGER.info("Copy mods keys from installed mods")
    
    # copy mods keys
    for mod_folder in os.listdir(SERVER_MODS_FOLDER):
        keys_folder = SERVER_MODS_FOLDER / mod_folder / "keys"
        
        for key_filename in os.listdir(keys_folder):
            key_file = keys_folder / key_filename
            if key_file.is_file() and key_filename.endswith(".bikey"):
                shutil.copy(key_file, SERVER_MODS_KEYS_FOLDER / key_filename)

def reset_mods() -> None:
    LOGGER.info("Reset mods")
    
    shutil.rmtree(SERVER_MODS_FOLDER)
    
def process_mod(mod_folder: Path) -> None:
    LOGGER.debug(f"Fix upper-cases linux bug for files of mod '{mod_folder}'")
    
    # fix upper case for Addons folder to addons
    if (mod_folder / "Addons").exists():
        os.rename(mod_folder / "Addons", mod_folder / "addons")
        
    # fix upper case for Keys folder to keys
    if (mod_folder / "Keys").exists():
        os.rename(mod_folder / "Keys", mod_folder / "keys")
    
    # fix upper case for mod addons pbo files
    for addon_filename in os.listdir(mod_folder / "addons"):
        addon_file = mod_folder / "addons" / addon_filename
        
        if addon_file.is_file():
            if addon_filename.endswith(".pbo"):
                os.rename(addon_file, mod_folder / "addons" / addon_filename.lower())
            if addon_filename.endswith(".bisign"):
                splitted_filename = addon_filename.split(".pbo")
                
                os.rename(addon_file, mod_folder / "addons" / f"{splitted_filename[0].lower()}.pbo{splitted_filename[1]}")
    
def install_mods() -> None:
    if not MODS_CONFIG_FILE.exists():
        LOGGER.debug("No mods to download or process")
        return
    
    LOGGER.debug("Read mods config file")
    
    with open(MODS_CONFIG_FILE, "r") as config_file:
        # this dictionary is equal to {mod_id: mod_name, ...}
        mods: dict[str, str] = json.loads(config_file.read())
        
    LOGGER.debug(f"Mods in config file : {mods}")
    
    LOGGER.info("Download and process mods")
    
    for mod_id, mod_name in mods.items():
        command = (
            "/steamcmd/steamcmd.sh",
            f"+force_install_dir {TMP_MODS_FOLDER}",
            f"+login {STEAM_USER} {STEAM_PASSWORD}",
            f"+workshop_download_item 107410 {mod_id}",
            "+quit"
        )
        
        command_for_logs = ' '.join(command).replace(STEAM_PASSWORD, "********")
        
        LOGGER.debug(f"Command to download mods '{mod_name}' with steam id '{mod_id}' from steam : '{command_for_logs}'")
        
        subprocess.call(command)
        
        LOGGER.debug(f"Copy mod '{mod_name}' at path '{SERVER_MODS_FOLDER / mod_name}'")
            
        shutil.copytree(TMP_MODS_FOLDER / "steamapps" / "workshop" / "content" / "107410" / mod_id, SERVER_MODS_FOLDER / mod_name)
        
        process_mod(SERVER_MODS_FOLDER / mod_name)

    shutil.rmtree(TMP_MODS_FOLDER)
    
    copy_mods_keys()