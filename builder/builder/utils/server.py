from logging import getLogger
import os
import shutil
import subprocess

from builder.utils.mission import install_mission
from builder.utils.servermods import install_servermod
from builder.utils.env import CONFIGS_FOLDER, MISSIONS_FOLDER, SERVER_CONFIG_FILE_NAME, SERVER_FOLDER, SERVER_MISSIONS_FOLDER, SERVER_SERVERMODS_FOLDER, SERVERMODS_FOLDER, STEAM_PASSWORD, STEAM_USER
from builder.utils.database import has_database, install_database, replace_env_vars_in_file

LOGGER = getLogger()

def reset_server() -> None:
    LOGGER.info("Reset Arma 3 server")
    
    for filename in os.listdir(SERVER_FOLDER):
        file = SERVER_FOLDER / filename
        
        if file.is_dir():
            shutil.rmtree(file)
        else:
            os.remove(file)

def install_server() -> None:
    LOGGER.info("Download and install Arma 3 server")
    
    command = (
        "/steamcmd/steamcmd.sh",
        f"+force_install_dir {SERVER_FOLDER}",
        f"+login {STEAM_USER} {STEAM_PASSWORD}",
        "+app_update 233780",
        "+quit",
    )
    
    command_for_logs = ' '.join(command).replace(STEAM_PASSWORD, "********")
    
    LOGGER.debug(f"Command to download server Arma 3 from steam : '{command_for_logs}'")
    
    subprocess.call(command)
    
def load_server_files() -> None:
    LOGGER.info("Load server files")
    
    LOGGER.debug(f"Load server config file at '{SERVER_FOLDER / SERVER_CONFIG_FILE_NAME}'")
    
    # copy server config file
    shutil.copy(CONFIGS_FOLDER / SERVER_CONFIG_FILE_NAME, SERVER_FOLDER / SERVER_CONFIG_FILE_NAME)
    
    replace_env_vars_in_file(SERVER_FOLDER / SERVER_CONFIG_FILE_NAME)
    
    if has_database():
        install_database()
        
    for servermod_folder in os.listdir(SERVERMODS_FOLDER):
        install_servermod(servermod_folder)
        
    for mission_folder in os.listdir(MISSIONS_FOLDER):
        install_mission(mission_folder)
        
    
def reset_server_files() -> None:
    LOGGER.info("Reset server files")
    
    if (SERVER_FOLDER / SERVER_CONFIG_FILE_NAME).exists():
        LOGGER.debug(f"Remove server config file at '{SERVER_FOLDER / SERVER_CONFIG_FILE_NAME}'")
        os.remove(SERVER_FOLDER / SERVER_CONFIG_FILE_NAME)
        
    if SERVER_SERVERMODS_FOLDER.exists():
        LOGGER.debug(f"Remove server mods folder at '{SERVER_SERVERMODS_FOLDER}'")
        shutil.rmtree(SERVER_SERVERMODS_FOLDER)
        
    if SERVER_MISSIONS_FOLDER.exists():
        LOGGER.debug(f"Remove mpmissions folder at '{SERVER_SERVERMODS_FOLDER}'")
        shutil.rmtree(SERVER_MISSIONS_FOLDER)
        