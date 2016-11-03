############
# rsyncFTP #
############

# TODO : Appliquer la structure de la 2e fonction à la 1ere
# ____________________________________________________________________________________________________
# Config

# Import
import logger
import argparse


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation
def initVariables(logger):
    """
    Fonction qui initialise le logger et les variables en fonction de ce que l'utilisateur a entre.
    La fonction genere une info recapitulant la liste des parametres entres.
    :param logger: logger
    :type logger: log
    :return: ARGS
    :rtype: list ?
    """
    # initialisation du logger
    logger.initLog()

    # initialisation du argparse
    PARSER = argparse.ArgumentParser(description='Dossier miroir avec "rsyncFTP"')
    # obligatoire
    PARSER.add_argument("dp", type=str, help="path to the directory")
    PARSER.add_argument("lp", type=str, help="path where to generate log")
    PARSER.add_argument("logConf", type=str, help="path to the configuration file of the logger")
    # optionnel
    PARSER.add_argument("-d", "--depth", default=2, help="depth of the surpervision directory, default = 2")
    PARSER.add_argument("-f", "--frequence", default=1, help="add supervision frequency in hz, default = 1 hz")
    PARSER.add_argument("-st", "--supervisionTime", default=60, help="add supervision time (in sec), default = 60 sec")

    # affichage des arguments rentres dans le log
    ARGS = PARSER.parse_args()
    logger.info(
        ":\npath to the directory where to save the downloaded website: %s\n" + \
        "url of the website to download: %s \npath to the configuration file of the logger: %s\n" + \
        "depth of the tree: %d\nmax size of a downloadable file: %d\nsize max of the directory where to download the website: %d\n",
        ARGS.savePath, ARGS.url, ARGS.logConf, ARGS.depth, ARGS.sizeFile, ARGS.sizeDirectory)

    return ARGS
