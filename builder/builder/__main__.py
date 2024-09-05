from argparse import ArgumentParser
from logging import getLogger
import os

from builder.utils.runner import get_starting_command
from builder.utils.env import SERVER_FOLDER, SERVER_MODS_FOLDER
from builder.utils.mods import install_mods, reset_mods
from builder.utils.server import install_server, reset_server, load_server_files, reset_server_files
from builder.utils.logger import setup_logger


if __name__ == "__main__":
    LOGGER = getLogger()

    parser = ArgumentParser(
        "arma_3_server_builder",
        description="Script to build an Arma 3 server",
    )

    parser.add_argument("-d", "--debug", action="store_true", help="Add this argument for run script in debug mode")
    
    parser.add_argument("-s", "--server", action="store_true", help="Add this argument for reset Arma 3 server files")
    parser.add_argument("-m", "--mods", action="store_true", help="Add this argument for reset mods downloaded from steam")

    args = parser.parse_args()

    setup_logger(args.debug)
    
    LOGGER.info("Builder started")
    
    if args.server:
        reset_server()
    
    if args.server or not (SERVER_FOLDER / "arma3server_x64").exists():
        install_server()
    else:
        LOGGER.info("Arma 3 server already exist and installed")
        
    if args.mods:
        reset_mods()
        
    if args.mods or not SERVER_MODS_FOLDER.exists():
        install_mods()
    else:
        LOGGER.info("Mods already exist and downloaded from steam")
        
    reset_server_files()
    
    load_server_files()
       
    starting_command = get_starting_command()
    
    LOGGER.info(f"Run this command to start Arma 3 server : '{starting_command}'")
    
    os.system(starting_command)