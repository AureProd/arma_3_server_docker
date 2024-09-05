import os
from builder.utils.env import ARMA_PARAMS, SERVER_MODS_FOLDER, SERVER_SERVERMODS_FOLDER


def get_starting_command() -> str:
    mods_names = [
        f"mods/{mod_folder}"
        for mod_folder in os.listdir(SERVER_MODS_FOLDER)
    ]
    servermods_names = [
        f"servermods/{servermod_folder}"
        for servermod_folder in os.listdir(SERVER_SERVERMODS_FOLDER)
    ]
    
    separator = "\;"
    
    command_parts = (
        "./arma3server_x64",
        "" if ARMA_PARAMS is None else ARMA_PARAMS,
        "-config=server.cfg",
        "-name=server",
        f"-mod={separator.join(mods_names)}",
        f"-servermod={separator.join(servermods_names)}"
    )
    
    return " ".join(command_parts)