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

def init(args):
    """
    Initialise les variables et constantes utiles
    :param args:
    :type args: dict
    :return:    ftp, dp, lp, includes, excludes, logconf, \
                profondeur, sizeFile, frequence, supervisionTime, \
                arbrePrecedent, startinglevel
    :rtype: tuple
    """
    # initialisation des constantes entrees en arguments
    ftp = {'hote': args.ftp[0], 'idt': args.ftp[1], 'mdp': args.ftp[2]}
    dp = args.dp
    includes = args.ie[0].split(',')
    excludes = args.ie[1].split(',')

    logPath = args.logPath
    logConf = args.logConf
    profondeur = args.profondeur
    sizeFile = args.sizeFile
    frequence = args.frequence
    supervisionTime = args.supervisionTime

    # initialisation des variable utiles pour la supervision
    arbrePrecedent = directorySupervisor.createSurveyList(list(os.walk(dp)))
    startinglevel = dp.count(os.sep)  # indique le niveau de profondeur initiale

    return ftp, dp, includes, excludes, logPath, logConf, \
           profondeur, sizeFile, frequence, supervisionTime, \
           arbrePrecedent, startinglevel


# ___________________________________________________________________________________________________
# Fonctions principales

def loop(args, logger):
    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    # === Initialisation des variables ===
    ARGS = parser.initVariables()
    FTP, DP, LP, INCLUDES, EXCLUDES, LOGCONF, \
    PROFONDEUR, SIZEFILE, FREQUENCE, SUPERVISIONTIME, \
    arbrePrecedent, STRATINGLEVEL = init(ARGS)
    # === Initialisation du logger ===
    MAIN_LOGGER = logger.initLog(LP, LOGCONF)
    # ecriture des parametres initiaux dans le logger
    parser.logArgs(ARGS, MAIN_LOGGER)
    # === Boucle principale ===
    loop(ARGS, MAIN_LOGGER)


if __name__ == "__main__":
    monMain()
