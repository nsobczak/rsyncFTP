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
    # initialisation des constantes entrees en arguments
    ftp = {'hote':args.ftp[0], 'idt':args.ftp[1], 'mdp':args.ftp[2]}
    dp = args.dp
    lp = args.lp
    includes = args.ie[0].split(',')
    excludes = args.ie[1].split(',')

    logconf = args.logConf
    profondeur = args.profondeur
    sizeFile = args.sizeFile
    frequence = args.frequence
    supervisionTime = args.supervisionTime

    # initialisation des variable utiles pour la supervision
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
