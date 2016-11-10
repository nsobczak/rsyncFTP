############
# rsyncFTP #
############

# TODO : Completer le programme
# ____________________________________________________________________________________________________
# Config

# Import
import logger
import parser
import directorySupervisor
import gestionFTP
import sys
import os
import time


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation

def init(logPath):
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    """


# ___________________________________________________________________________________________________
# Fonctions principales

def loop(logger, args):


    return 1

# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    MAIN_LOGGER = logger.initLog()
    ARGS = parser.initVariables(MAIN_LOGGER)
    loop(MAIN_LOGGER, ARGS)


if __name__ == "__main__":
    monMain()
