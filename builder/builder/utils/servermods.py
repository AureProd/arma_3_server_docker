from logging import getLogger
import os
import shutil

from builder.utils.pbo import pack_in_pbo
from builder.utils.env import SERVER_SERVERMODS_FOLDER, SERVERMODS_FOLDER

LOGGER = getLogger()

def install_servermod(servermod_folder: str) -> None:
    LOGGER.info(f"Install servermod '{servermod_folder}'")
    
    LOGGER.debug(f"Copy servermod '{servermod_folder}' at '{SERVER_SERVERMODS_FOLDER / servermod_folder}'")
    
    # copy server mod
    shutil.copytree(SERVERMODS_FOLDER / servermod_folder, SERVER_SERVERMODS_FOLDER / servermod_folder)
    
    for addon_folder in os.listdir(SERVER_SERVERMODS_FOLDER / servermod_folder / "addons"):
        LOGGER.debug(f"Pack in PBO addon '{addon_folder}' of servermod '{servermod_folder}'")
        
        pack_in_pbo(SERVER_SERVERMODS_FOLDER / servermod_folder / "addons" / addon_folder)