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
    PARSER.add_argument("ftp", type=tuple, help="(hote, identifiant, mot_de_passe, port) donnees pour le site FTP distant")
    PARSER.add_argument("dp", type=str, help="chemin vers le dossier local")
    PARSER.add_argument("lp", type=str, help="chemin pour generer le log")
    PARSER.add_argument("inEx", type=list, help="liste de fichiers à inclure (les extensions)")
    PARSER.add_argument("exEx", type=list, help="liste de fichiers à exclure (les extensions)")
    # optionnel
    PARSER.add_argument("-lc", "--logConf", default="rsyncFTP.conf", help="chemin vers le fichier conf du log (gestion des handler")
    PARSER.add_argument("-p", "--profondeur", default=2, help="profondeur de la suppervision du dossier, default = 2")
    PARSER.add_argument("-f", "--frequence", default=60, help="frequence de suppervision du dossier et de refraichissement du site ftp en secondes, default = 60 sec")
    PARSER.add_argument("-st", "--supervisionTime", default=-1, help="ajoute un temps de suppervision (in sec), default = -1 (infinit time)")

    # affichage des arguments rentres dans le log
    ARGS = PARSER.parse_args()
    logger.info(
        ":\npath to the directory where to save the downloaded website: %s\n" + \
        "url of the website to download: %s \npath to the configuration file of the logger: %s\n" + \
        "depth of the tree: %d\nmax size of a downloadable file: %d\nsize max of the directory where to download the website: %d\n",
        ARGS.savePath, ARGS.url, ARGS.logConf, ARGS.depth, ARGS.sizeFile, ARGS.sizeDirectory)

    return ARGS


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    MAIN_LOGGER = logger.initLog()
    ARGS = initVariables(MAIN_LOGGER)

if __name__ == "__main__":
    monMain()


