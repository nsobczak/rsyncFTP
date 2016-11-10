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

def init(logger, args):
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    """
    dp = args.dp
    lp = args.lp
    depth = int(args.depth)
    frequence = int(args.frequence)
    supervisionTime = int(args.supervisionTime)
    arbrePrecedent = directorySupervisor.createSurveyList(list(os.walk(dp)))
    startinglevel = dp.count(os.sep)  # indique le niveau de profondeur initiale
    return arbrePrecedent


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
