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
def initVariables():
    """
    Fonction qui initialise le logger et les variables en fonction de ce que
    l'utilisateur a entre.
    La fonction genere une info recapitulant la liste des parametres entres.
    :return: ARGS
    :rtype: dict
    """
    # initialisation du argparse
    PARSER = argparse.ArgumentParser(description='Dossier miroir avec "rsyncFTP"')
    # obligatoire
    PARSER.add_argument("ftp", type=str, nargs=3,
                        help="(hote, identifiant, mot_de_passe) :\n" + \
                             "donnees pour le site FTP distant",
                        )
    PARSER.add_argument("dp", type=str, help="chemin vers le dossier local")
    PARSER.add_argument("lp", type=str, help="chemin pour generer le log")
    PARSER.add_argument("ie", type=str, nargs=2,
                        help="2-uple contenant :\n" +
                             "-la liste de fichiers a inclure (les extensions)\n" + \
                             "-la liste de fichiers a inclure (les extensions)\n" + \
                             "sous la forme . " + \
                             "ex : ([],['txt']) pour dire de tout inclure sauf les txt")
    # optionnel
    PARSER.add_argument("-lc", "--logConf", default="rsyncFTP.conf",
                        help="chemin vers le fichier conf du log (gestion des handler)")
    PARSER.add_argument("-p", "--profondeur", default=2,
                        help="profondeur de la supervision du dossier, default = 2")
    PARSER.add_argument("-sf","--sizeFile",default=500,
                        help="taille maximale des fichiers transferes en Mo, default = 500 Mo")
    PARSER.add_argument("-f", "--frequence", default=1,
                        help="frequence de supervision en s, default = 1 s")
    PARSER.add_argument("-st", "--supervisionTime", default=60,
                        help="temps de supervision en s, default = 60 sec")

    # affichage des arguments rentres dans le log
    ARGS = PARSER.parse_args()

    # log.info(
    #     ":\n(hote, identifiant, mot_de_passe, (port)) " +\
    #     "donnees pour le site FTP distant: %s \n" + \
    #     "chemin vers le dossier local: %s \n" + \
    #     "chemin pour generer le log: %s \n" + \
    #     "2-uple contenant :\n" +
    #     "-la liste de fichiers a inclure (les extensions): %s \n" + \
    #     "-la liste de fichiers a inclure (les extensions): %s \n" +\
    #     "chemin vers le fichier conf du log (gestion des handler): %s \n" + \
    #     "profondeur de la supervision du dossier: %d \n" + \
    #     "taille maximale des fichiers transferes en Mo: %d \n" + \
    #     "frequence de supervision en s: %d \n" + \
    #     "temps de supervision en s: %d \n",
    #     ARGS.ftp, ARGS.dp, ARGS.lp, str(ARGS.ie[0]), str(ARGS.ie[1]),
    #     ARGS.logConf, ARGS.profondeur, ARGS.sizeFile, ARGS.frequence,
    #     ARGS.supervisionTime)
    return ARGS


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    MAIN_LOGGER = logger.initLog()
    ARGS = initVariables()
    print(ARGS)

if __name__ == "__main__":
    monMain()


