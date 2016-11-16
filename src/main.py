############
# rsyncFTP #
############
# main     #
############

# TODO : Faire la boucle principale
# ____________________________________________________________________________________________________
# Config

# Import
import logger
import parser
import directorySupervisor
import gestionFTP
import os


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation

def init(args):
    """
    Initialise les variables, constantes utiles, et se connecte au serveur ftp
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

    # connexion au serveur FTP
    gestionFTP.connectionAuServeurFTP(ftp['hote'], ftp['idt'], args.ftp['mdp'])

    return ftp, dp, includes, excludes, logPath, logConf, \
           profondeur, sizeFile, frequence, supervisionTime, \
           arbrePrecedent, startinglevel


# ___________________________________________________________________________________________________
# Fonctions principales
def updateFTP():
    """
    Fonction qui gere la mise a jour du dossier distant
    :return:
    """
    #Si ajout d'un fichier

    #Si suppression d'un fichier

    #Si ajout d'un dossier

    #Si suppression d'un dossier

    #Si modification d'un fichier => remplacement

    #Si modification d'un dossier

    return 1


def loop(args, logger):
    """
    Fonction de boucle principale
    :param args:
    :param logger:
    :type args: dict
    :type logger: log
    :return: 1
    """
    # Sureveiller
    #directorySupervisor.loop(logger, args.frequence, args.supervisionTime, args.arbrePrecedent, args.dp)
    # Si modif, mettre a jour le serveur FTP
    #updateFTP()

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
