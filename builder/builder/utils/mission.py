
from logging import getLogger
import shutil

from builder.utils.env import MISSIONS_FOLDER, SERVER_MISSIONS_FOLDER
from builder.utils.pbo import pack_in_pbo


LOGGER = getLogger()

def install_mission(mission_folder: str) -> None:
    LOGGER.info(f"Install mission '{mission_folder}'")
    
    LOGGER.debug(f"Copy mission '{mission_folder}' at '{SERVER_MISSIONS_FOLDER / mission_folder}'")
    
    # copy mission folder
    shutil.copytree(MISSIONS_FOLDER / mission_folder, SERVER_MISSIONS_FOLDER / mission_folder)
    
    LOGGER.debug(f"Pack in PBO mission '{mission_folder}'")
        
    pack_in_pbo(SERVER_MISSIONS_FOLDER / mission_folder)