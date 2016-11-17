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
import time


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation

def init(args):
    """
    Initialise les variables, constantes utiles, et se connecte au serveur ftp
    :param args: parametres entres en lignes de commandes
    :type args: dict
    :return: connectFTP, includes, excludes, arbrePrecedent, startinglevel
    :rtype: tuple
    """
    # initialisation des constantes entrees en arguments
    ftp = {'hote': args.ftp[0], 'idt': args.ftp[1], 'mdp': args.ftp[2]}
    includes = args.ie[0].split(',')
    excludes = args.ie[1].split(',')
    # initialisation des variable utiles pour la supervision
    startinglevel = args.dp.count(os.sep)  # indique le niveau de profondeur initiale
    arbrePrecedent = directorySupervisor.createSurveyList(list(os.walk(args.dp)), startinglevel, args.profondeur)

    # connexion au serveur FTP
    connectFTP = gestionFTP.connectionAuServeurFTP(ftp['hote'], ftp['idt'], ftp['mdp'])

    return connectFTP, includes, excludes, arbrePrecedent, startinglevel


# ___________________________________________________________________________________________________
# Fonctions principales

def updateFTP_M(args, logger, connectFTP, M):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param M: liste des elements modifies
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type M: list
    """
    for tup in M:
        path = tup[0]
        # Si modification d'un fichier => remplacement
        if os.path.isfile(path):
            fichier_chemin_absolu, fichier_nom = os.path.split(path)
            fichier_chemin_relatif = os.path.realpath(fichier_chemin_absolu,args.dp)
            gestionFTP.supprimerFichier(ftp=connectFTP, fichier_chemin=fichier_chemin_relatif, fichier_nom=fichier_nom)
            gestionFTP.envoyerUnFichier(ftp=connectFTP, fichier_chemin=path, fichier_nom=fichier_nom)
        # Les modifications de dossiers ne sont pas prises en compte ici
        # car elles sont assimilees a une suppression et creation
        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP_A(args, logger, connectFTP, A):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param A: liste des elements ajoutes
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type A: list
    """
    for tup in A:
        path = tup[0]
        # Si ajout d'un fichier
        if os.path.isfile(path):
            fichier_chemin_absolu, fichier_nom = os.path.split(path)
            gestionFTP.envoyerUnFichier(fichier_chemin=path, ftp=connectFTP, fichier_nom=fichier_nom)
        # Si ajout d'un dossier
        elif os.path.isdir(path):
            print("coucou")
            # chemin local et nom dossier a recuperer en separant le chhemin absolu
            # gestionFTP.copierContenuDossier(ftp=connectFTP, chemin_ftp="", chemin_local=, nom_dossier=,
            #                                 profondeure_copie_autorisee=args.profondeur)
        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP_D(args, logger, connectFTP, D):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args:
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param D: liste des elements supprimes
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type D: list
    """
    for tup in D:
        path = tup[0]
        # Si suppression d'un fichier
        if os.path.isfile(path):
            gestionFTP.effacerFichier(ftp=connectFTP, fichier=path)
        # Si suppression d'un dossier
        elif os.path.isdir(path):
            # gestionFTP.supprimerDossier(ftp=connectFTP, dossier=)
            print("coucou")
        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP(args, logger, connectFTP, M, A, D):
    """
    Fonction qui gere la mise a jour du dossier distant
    :param args:
    :param logger:
    :type args: dict
    :type logger: log
    :param connectFTP: objet ftp
    :type connectFTP: class 'ftplib.FTP'
    """
    # Si ajout
    if (A != []):
        updateFTP_A(args, logger, connectFTP, A)
    # Si suppression
    if (D != []):
        updateFTP_D(args, logger, connectFTP, D)
    # Si modification
    if (M != []):
        updateFTP_M(args, logger, connectFTP, M)


# ____________________________________________________________________________________________________
def loop(args, logger, arbrePrecedent, connectFTP):
    """
    Fonction de boucle principale. Elle fonctionne en 2 actions:
    - Surveiller
    - Si modif, mettre a jour le serveur FTP
    :param args:
    :param logger:
    :type args: dict
    :type logger: log
    :param connectFTP: objet ftp
    :type connectFTP: class 'ftplib.FTP'


    :return: 1
    """
    # Var
    frequence = args.frequence
    supervisionTime = args.supervisionTime
    dp = args.dp

    # boucle infinie si supervision time = -1
    infinite = False
    if (supervisionTime == -1):
        logger.info("supervisionTime = -1 => supervision en continue")
        infinite = True

    # initialisation du timer
    totalTime = 0
    oldTime = time.time()
    newTime = time.time()

    # boucle de synchronisation du dossier miroir
    while totalTime < (supervisionTime * frequence) or infinite:
        newTime = time.time()
        if (newTime - oldTime) > (1 / frequence):
            logger.debug(str(totalTime / frequence) + " sec depuis lancement du programme")
            oldTime = time.time()
            nouvelArbre = directorySupervisor.createSurveyList(list(os.walk(dp)))
            M, A, D = directorySupervisor.comparateSurveyList(arbrePrecedent, nouvelArbre)
            # si modifications effectuees
            if len(M) or len(A) or len(D):
                arbrePrecedent = nouvelArbre
                directorySupervisor.logTheMADLists(M, A, D)
                updateFTP(args, logger, connectFTP, M, A, D)
            totalTime += 1

    return 1


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    # === Initialisation des variables ===
    a = prftp.test

    ARGS = prftp.initVariables()
    buffer = init(ARGS)
    connectFTP = buffer[0]
    INCLUDES = buffer[1]
    EXCLUDES = buffer[2]
    arbrePrecedent = buffer[3]
    STARTINGLEVEL = buffer[4]
    # === Initialisation du logger ===
    MAIN_LOGGER = logger.initLog(ARGS.logPath, ARGS.logConf)
    # ecriture des parametres initiaux dans le logger
    prftp.logArgs(ARGS, MAIN_LOGGER)
    # === Boucle principale ===
    loop(ARGS, MAIN_LOGGER, arbrePrecedent, connectFTP)


if __name__ == "__main__":
    monMain()
