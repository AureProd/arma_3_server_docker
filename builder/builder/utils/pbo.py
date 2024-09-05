from logging import getLogger
from pathlib import Path
import shutil
import subprocess


LOGGER = getLogger()

def pack_in_pbo(folder_to_pack: Path) -> Path:
    LOGGER.info(f"Pack in PBO folder '{folder_to_pack}'")
    
    pbo_file = Path(f"{folder_to_pack}.pbo")
        
    command = (
        "makepbo",
        "-N", 
        str(folder_to_pack)
    )
    
    command_for_logs = ' '.join(command)
    
    LOGGER.debug(f"Command to pack in PBO the folder : '{command_for_logs}'")
    
    subprocess.call(command)
    
    if not pbo_file.exists():
        LOGGER.error(f"Packing in PBO of folder '{folder_to_pack}' has failed")
        exit(1)
    
    shutil.rmtree(folder_to_pack)
    
    LOGGER.info(f"Success of packing in PBO in file '{pbo_file}'")
    
    return pbo_file