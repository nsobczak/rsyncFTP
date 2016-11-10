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
    Fonction qui initialise le logger et les variables en fonction de ce que
    l'utilisateur a entre.
    La fonction genere une info recapitulant la liste des parametres entres.
    :param logger: logger
    :type logger: log
    :return: ARGS
    :rtype: dict
    """
    # initialisation du logger
    logger.initLog()

    # initialisation du argparse
    PARSER = argparse.ArgumentParser(description='Dossier miroir avec "rsyncFTP"')
    # obligatoire
    PARSER.add_argument("ftp", type=tuple,
                        help="(hote, identifiant, mot_de_passe, port) :\n" + \
                             "donnees pour le site FTP distant")
    PARSER.add_argument("dp", type=str, help="chemin vers le dossier local")
    PARSER.add_argument("lp", type=str, help="chemin pour generer le log")
    PARSER.add_argument("-ie", "--includeOrExcludeExtension", type=tuple,
                        help="2-uple contenant :\n" +
                             "-la liste de fichiers à inclure (les extensions)\n" + \
                             "-la liste de fichiers à inclure (les extensions)")
    # optionnel
    PARSER.add_argument("-lc", "--logConf", default="rsyncFTP.conf",
                        help="chemin vers le fichier conf du log (gestion des handler")
    PARSER.add_argument("-p", "--profondeur", default=2,
                        help="profondeur de la supervision du dossier, default = 2")
    PARSER.add_argument("-f", "--frequence", default=1,
                        help="frequence de supervision en s, default = 1 s")
    PARSER.add_argument("-st", "--supervisionTime", default=60,
                        help="temps de supervision en s, default = 60 sec")

    # affichage des arguments rentres dans le log
    ARGS = PARSER.parse_args()
    logger.info(
        ":\npath to the directory where to save the downloaded website: %s\n" + \
        "url of the website to download: %s \n" + \
        "path to the configuration file of the logger: %s\n" + \
        "depth of the tree: %d\nmax size of a downloadable file: %d\n" + \
        "size max of the directory where to download the website: %d\n",
        ARGS.savePath, ARGS.url, ARGS.logConf, ARGS.depth, ARGS.sizeFile, ARGS.sizeDirectory)

    return ARGS


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    MAIN_LOGGER = logger.initLog()
    ARGS = initVariables(MAIN_LOGGER)
    print(ARGS)

if __name__ == "__main__":
    monMain()


