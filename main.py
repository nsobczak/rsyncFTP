############
# rsyncFTP #
############

# TODO : Remplacer les noms des fonctions arbre par des noms francais + creer fonction loop
# ____________________________________________________________________________________________________
# Config

# Import
import logging
import sys
import argparse
import os
import time

# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Variables globales


dp = None
lp = None
depth = None
frequence = None
arbrePrecedent = None
startinglevel = None
logger = None
supervisionTime = None


# ____________________________________________________________________________________________________
# Fonctions d'initialisation

def initLog(logPath):
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    """
    logging.basicConfig(
        filename=logPath + "/DirectorySupervisor.log", \
        datefmt="%d/%m/%Y-%H:%M:%S", \
        format="%(asctime)s %(levelname)s %(funcName)s %(message)s", \
        level=logging.INFO)     # 'filename': '/path/to/DirectorySupervisor.debug.log',
    logging.info("Programme lance")


def initVariablesGlobales():
    """
    Fonction qui initialise les variables globales en fonction de ce que l'utilisateur a entre.
    La fonction genere une info recapitulant la liste des parametres entres.
    """
    global dp
    global lp
    global depth
    global frequence
    global supervisionTime
    global startinglevel
    global arbrePrecedent

    parser = argparse.ArgumentParser(description='Supervision de dossier with DirectorySupervisor')
    # obligatoire
    parser.add_argument("dp", type=str, help="path to the directory")
    parser.add_argument("lp", type=str, help="path where to generate log")
    # optionnel
    parser.add_argument("-d", "--depth", default=2, help="depth of the surpervision directory, default = 2")
    parser.add_argument("-f", "--frequence", default=1, help="add supervision frequency in hz, default = 1 hz")
    parser.add_argument("-st", "--supervisionTime", default=60, help="add supervision time (in sec), default = 60 sec")

    # initialisation des parametres globaux
    args = parser.parse_args()
    dp = args.dp
    lp = args.lp
    depth = int(args.depth)
    frequence = int(args.frequence)
    supervisionTime = int(args.supervisionTime)
    startinglevel = dp.count(os.sep)        # indique le niveau de profondeur initiale
    arbrePrecedent = createSurveyList(list(os.walk(dp)))


def afficheArgument():
    """affichage des arguments rentres"""
    logging.info(
        ":\npath to the directory : %s \npath where to generate log : %s \ndepth of the directory : %s \nfrequency : %s hz \nsupervision time : %s sec\n",
        dp, lp, depth, frequence, supervisionTime)


# ___________________________________________________________________________________________________
# Fonctions de creation de l'arbre du dossier et de comparaison



# ___________________________________________________________________________________________________
# Fonctions principales

def loop():



# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    loop()


if __name__ == "__main__":
    monMain()
