"""
############
# rsyncFTP #
############
# main     #
############

@author: Julien Vermeil and Vincent Reynaert and Nicolas Sobczak
"""

# TODO : Faire la boucle principale de synchronisation, gerer les exceptions
# %%__________________________________________________________________________________________________
# Config

# Import
import logger
import parserRsyncFTP as prftp
import directorySupervisor
import gestionFTP
import os
import time


# %%__________________________________________________________________________________________________
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


def initialisationDossierFTP(args, logger, connectFTP):
    """
    Fonction qui initialise le dossier sur le serveur FTP : supprime puis copie le dossier local
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    """
    dossier_chemin_absolu, dossier_nom = os.path.split(args.dp)
    suppression = gestionFTP.supprimerDossier(ftp=connectFTP, dossier_chemin="", dossier_nom=dossier_nom)
    if not suppression:
        logger.debug('Le dossier est bien supprime.')
    else:
        logger.debug("Le dossier n'a pas pu etre supprime car il n'existe pas.")
    gestionFTP.copierContenuDossier(ftp=connectFTP, chemin_ftp="", chemin_local=args.dp, nom_dossier=dossier_nom,
                                    profondeure_copie_autorisee=args.profondeur)
    logger.info("initialisation du dossier")


# %%_________________________________________________________________________________________________
# Fonctions principales
def donneCheminRelatif(args, chemin_element):
    """
    Fonction qui retourne le chemin relatif a partir des chemins absolus du dossier surveille et de l'element dont on veut le chemin relatif
    :param args: parametres entres en lignes de commandes
    :param chemin_element: chemin absolu vers l'element (fichier ou dossier) dont on veut le chemin relatif
    :type args: dict
    :type chemin_element: str
    :return: chemin_relatif
    :rtype: str
    """
    chemin_absolu, nom = os.path.split(args.dp)
    longueur_chemin_absolu = len(chemin_absolu)
    chemin_relatif = chemin_element[longueur_chemin_absolu:]
    return chemin_relatif


def isFileToBeIncluded(includes, excludes, nom_fichier):
    """
    Fonction qui retourne vrai si le fichier a une extension que l'on souhaite copier
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :param nom_fichier: nom du fichier avec son extension
    :type nom_fichier: str
    :return: result
    :rtype: bool
    """
    result = False
    # on recupere l'extension du fichier
    root, extension = os.path.splitext(nom_fichier)

    # cas 1 : on inclut toutes les extensions sauf certaines
    if ((includes[0] == "*") and (not extension in excludes)):
        result = True
    # cas 2 : on exclut toutes les extensions sauf certaines
    else:
        if ((excludes[0] == "*") and (extension in includes)):
            result = True

    return result


def updateFTP_M(args, logger, connectFTP, includes, excludes, M):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :param M: liste des elements modifies
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type includes: list
    :type excludes: list
    :type M: list
    """
    for tup in M:
        path = tup[0]

        # Si modification d'un fichier => remplacement
        if os.path.isfile(path):
            fichier_chemin_absolu, fichier_nom = os.path.split(path)
            # Si l'extension du fichier est a inclure
            if isFileToBeIncluded(includes, excludes, fichier_nom):
                chemin_relatif = donneCheminRelatif(args, fichier_chemin_absolu)
                positionDeBaseFTP = connectFTP.pwd()
                gestionFTP.positionnementDansLeFTP(connectFTP, chemin_relatif)
                gestionFTP.supprimerFichier(ftp=connectFTP, fichier_chemin=chemin_relatif, fichier_nom=fichier_nom)
                gestionFTP.envoyerUnFichier(ftp=connectFTP, fichier_chemin=path, fichier_nom=fichier_nom)
                gestionFTP.positionnementDansLeFTP(connectFTP, positionDeBaseFTP)
        # Les modifications de dossiers ne sont pas prises en compte ici
        # car elles sont assimilees a une suppression suivie d'une creation
        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP_A(args, logger, connectFTP, includes, excludes, A):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :param A: liste des elements ajoutes
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type includes: list
    :type excludes: list
    :type A: list
    """
    for tup in A:
        path = tup[0]

        # Si ajout d'un fichier
        if os.path.isfile(path):
            fichier_chemin_absolu, fichier_nom = os.path.split(path)
            # Si l'extension du fichier est a inclure
            if isFileToBeIncluded(includes, excludes, fichier_nom):
                chemin_relatif = donneCheminRelatif(args, fichier_chemin_absolu)
                positionDeBaseFTP = connectFTP.pwd()
                gestionFTP.positionnementDansLeFTP(connectFTP, chemin_relatif)
                gestionFTP.envoyerUnFichier(fichier_chemin=path, ftp=connectFTP, fichier_nom=fichier_nom)
                gestionFTP.positionnementDansLeFTP(connectFTP, positionDeBaseFTP)
        # Si ajout d'un dossier
        elif os.path.isdir(path):
            # chemin local et nom dossier a recuperer en separant le chemin absolu
            dossier_chemin_absolu, dossier_nom = os.path.split(path)
            chemin_relatif = donneCheminRelatif(args, dossier_chemin_absolu)
            positionDeBaseFTP = connectFTP.pwd()
            gestionFTP.positionnementDansLeFTP(connectFTP, chemin_relatif)
            gestionFTP.copierContenuDossier(ftp=connectFTP, chemin_ftp="", chemin_local=path, nom_dossier=dossier_nom,
                                            profondeure_copie_autorisee=args.profondeur)
            gestionFTP.positionnementDansLeFTP(connectFTP, positionDeBaseFTP)

        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP_D(args, logger, connectFTP, includes, excludes, D):
    """
    Fonction qui s'occupe de mettre a jour le dossier situe sur le serveur FTP en cas d'ajout
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :param D: liste des elements supprimes
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type includes: list
    :type excludes: list
    :type D: list
    """
    for tup in D:
        path = tup[0]

        chemin_absolu, nom = os.path.split(path)
        chemin_relatif = donneCheminRelatif(args, chemin_absolu)
        try:
            # Si suppression dossier
            gestionFTP.supprimerDossier(ftp=connectFTP, dossier_chemin=chemin_relatif, dossier_nom=nom)
        except UnboundLocalError:
            # Si suppression fichier
            if isFileToBeIncluded(includes, excludes, nom):
                gestionFTP.supprimerFichier(ftp=connectFTP, fichier_chemin=chemin_relatif, fichier_nom=nom)

        else:
            logger.info(path + " n'est pas supporte par rsyncFTP")


def updateFTP(args, logger, connectFTP, includes, excludes, M, A, D):
    """
    Fonction qui gere la mise a jour du dossier distant
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param connectFTP: objet ftp
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :param M:
    :param A:
    :param D:
    :type args: dict
    :type logger: log
    :type connectFTP: class 'ftplib.FTP'
    :type includes: list
    :type excludes: list
    :type M: list
    :type A: list
    :type D: list
    :param connectFTP: objet ftp
    :type connectFTP: class 'ftplib.FTP'
    """
    # Si ajout
    if (A != []):
        updateFTP_A(args, logger, connectFTP, includes, excludes, A)
    # Si suppression
    if (D != []):
        updateFTP_D(args, logger, connectFTP, includes, excludes, D)
    # Si modification
    if (M != []):
        updateFTP_M(args, logger, connectFTP, includes, excludes, M)


# %%__________________________________________________________________________________________________
def loop(args, logger, arbrePrecedent, startingLevel, connectFTP, includes, excludes):
    """
    Fonction de boucle principale. Elle fonctionne en 2 actions:
    - Surveiller
    - Si modif, mettre a jour le serveur FTP
    :param args: parametres entres en lignes de commandes
    :param logger: fichier de log
    :param arbrePrecedent:
    :param startingLevel: niveau de profondeur de depart
    :param connectFTP: objet ftp
    :param includes: liste des fichiers a inclure
    :param excludes: liste des fichiers a exclure
    :type args: dict
    :type logger: log
    :type arbrePrecedent:
    :type startingLevel: int
    :type connectFTP: class 'ftplib.FTP'
    :type includes: list
    :type excludes: list
    :return: 1
    :rtype: int
    """
    # Var
    frequence = args.frequence
    supervisionTime = args.supervisionTime
    dp = args.dp

    # initialisation dossier sur serveur ftp
    initialisationDossierFTP(args, logger, connectFTP)

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
            nouvelArbre = directorySupervisor.createSurveyList(list(os.walk(dp)), startingLevel, args.profondeur)
            M, A, D = directorySupervisor.comparateSurveyList(arbrePrecedent, nouvelArbre)
            # si modifications effectuees
            if len(M) or len(A) or len(D):
                arbrePrecedent = nouvelArbre
                directorySupervisor.logTheMADLists(logger, M, A, D)
                updateFTP(args, logger, connectFTP, includes, excludes, M, A, D)
            totalTime += 1

    return 1


# %%__________________________________________________________________________________________________
# ____________________________________________________________________________________________________
def monMain():
    """Tests Unitaires
    print(isFileToBeIncluded(['*'], ['.odt', ".docx"], "/home/nicolas/Documents/fichier.docx"))
    print(isFileToBeIncluded(['*'], ['.odt', ".docx"], "/home/nicolas/Documents/fichier.txt"))
    print(isFileToBeIncluded(['.odt', ".docx"], ['*'], "/home/nicolas/Documents/fichier.docx"))
    print(isFileToBeIncluded(['.odt', ".docx"], ['*'], "/home/nicolas/Documents/fichier.txt"))
    """

    # === Initialisation des variables ===
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
    loop(ARGS, MAIN_LOGGER, arbrePrecedent, STARTINGLEVEL, connectFTP, INCLUDES, EXCLUDES)


if __name__ == "__main__":
    monMain()
