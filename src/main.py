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
import parserRsyncFTP as prftp
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
    includes = args.ie[0].split(',')
    excludes = args.ie[1].split(',')
    # initialisation des variable utiles pour la supervision
    startinglevel = args.dp.count(os.sep)  # indique le niveau de profondeur initiale
    arbrePrecedent = directorySupervisor.createSurveyList(list(os.walk(args.dp)),startinglevel,args.profondeur)

    # connexion au serveur FTP
    gestionFTP.connectionAuServeurFTP(ftp['hote'], ftp['idt'], ftp['mdp'])

    return ftp, includes, excludes, arbrePrecedent, startinglevel


# ___________________________________________________________________________________________________
# Fonctions principales
def updateFTP():
    """
    Fonction qui gere la mise a jour du dossier distant
    :return:
    """
    """
    #Si ajout d'un fichier
    gestionFTP.envoyerUnFichier(fichier_chemin=,fichier_nom=, ftp=, )
    #Si suppression d'un fichier
    gestionFTP.effacerFichier(ftp=, fichier=)
    #Si ajout d'un dossier
    gestionFTP.creerDossier(ftp=, nom_dossier=, chemin_dossier=)
    gestionFTP.copierContenuDossier(ftp=, chemin_ftp=, chemin_local=,nom_dossier=,profondeure_copie_autorisee=)
    #Si suppression d'un dossier
    gestionFTP.supprimerDossier(ftp=,dossier=)
    #Si modification d'un fichier => remplacement
    gestionFTP.effacerFichier(ftp=,fichier=)
    gestionFTP.envoyerUnFichier(ftp=,fichier_chemin=,fichier_nom=)
    #Si modification d'un dossier
    """
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
    #directorySupervisor.comparateSurveyList()
    # Si modif, mettre a jour le serveur FTP
    #updateFTP()

    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    # === Initialisation des variables ===
    a = prftp.test

    ARGS = prftp.initVariables()
    # buffer = init(ARGS)
    # ftp = buffer[0]
    # INCLUDES = buffer[1]
    # EXCLUDES = buffer[2]
    # arbrePrecedent = buffer[3]
    # STARTINGLEVEL = buffer[4]
    # # === Initialisation du logger ===
    # MAIN_LOGGER = logger.initLog(ARGS.logPath, ARGS.logConf)
    # # ecriture des parametres initiaux dans le logger
    # parser.logArgs(ARGS, MAIN_LOGGER)
    # # === Boucle principale ===
    # loop(ARGS, MAIN_LOGGER)


if __name__ == "__main__":
    monMain()
