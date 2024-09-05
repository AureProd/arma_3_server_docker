from logging import getLogger
import os
from pathlib import Path
import re
from builder.utils.env import EXTDB3_FOLDER, EXTDB3_SERVERMOD_NAME, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, SERVER_FOLDER, SERVER_SERVERMODS_FOLDER
import shutil

LOGGER = getLogger()

def has_database() -> bool:
    return (
        MYSQL_HOST is not None and 
        MYSQL_PORT is not None and     
        MYSQL_USER is not None and     
        MYSQL_PASSWORD is not None and     
        MYSQL_DATABASE is not None
    )
    
def replace_env_vars_in_file(file_path: Path) -> None:
    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace placeholders with environment variables
    def replace_placeholder(match):
        var_name = match.group(1)
        return os.getenv(var_name, match.group(0))  # Default to the placeholder if not found
    
    # Use regex to find placeholders like $VAR_NAME
    content = re.sub(r'\$(\w+)', replace_placeholder, content)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)
    
def install_database() -> None:
    LOGGER.info("Install and initialize database extdb3 server mod")
    
    # copy dll extdb3 files
    shutil.copy(EXTDB3_FOLDER / "tbbmalloc.dll", SERVER_FOLDER / "tbbmalloc.dll")
    shutil.copy(EXTDB3_FOLDER / "tbbmalloc_x64.dll", SERVER_FOLDER / "tbbmalloc_x64.dll")
                
    LOGGER.debug(f"Copy servermod '@extDB3' at '{SERVER_SERVERMODS_FOLDER / EXTDB3_SERVERMOD_NAME}'")
        
    # copy server mod extdb3
    shutil.copytree(EXTDB3_FOLDER / EXTDB3_SERVERMOD_NAME, SERVER_SERVERMODS_FOLDER / EXTDB3_SERVERMOD_NAME)
    
    replace_env_vars_in_file(SERVER_SERVERMODS_FOLDER / EXTDB3_SERVERMOD_NAME / "extdb3-conf.ini")