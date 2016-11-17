############
# rsyncFTP #
############
# logger   #
############

# TODO : /
# ____________________________________________________________________________________________________
# Config

# Import
import logging
import logging.config
import os
import os.path


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation
def creeLog(logPath):
    """
    Fonction qui cree le logger.
    - soit elle cree un fichier avec le nom qu'on lui indique,
    - soit elle crée un fichier dans le répertoire qu'on lui indique,
    - soit elle utilise le fichier .conf que nous avons cree.
    :param logPath: chemin ou enregistrer le logger ou nom du fichier que l'on veut creer.
    :return: MAIN_LOGGER
    :rtype: logger
    """
    if os.path.isdir(logPath):
        nameFile = os.path.join(logPath, "rsyncFTP.log")
    elif os.path.isfile(logPath):
        nameFile = logPath
    else:
        nameFile = "rsyncFTP.log"

    logging.basicConfig( \
        filename=nameFile, \
        datefmt="%d/%m/%Y-%H:%M:%S", \
        format="%(asctime)s %(levelname)s %(funcName)s %(message)s", \
        level=logging.INFO)  # 'filename': '/path/to/rsyncFTP.debug.log',
    MAIN_LOGGER = logging.getLogger("rsyncFTP")
    MAIN_LOGGER.info("Programme lance")

    return MAIN_LOGGER


def initLog(logPath, logConf):
    """
    Fonction qui initialise le logger.
    :param logPath: chemin ou enregistrer le logger
    :param logConf: chemin ou trouver le fichier .conf
    :return: MAIN_LOGGER
    :rtype: logger
    """
    if logPath == "":
        logging.config.fileConfig(logConf)
        # definition du handler de log principal
        MAIN_LOGGER = logging.getLogger("rsyncLocal")
        MAIN_LOGGER.info("Programme lance")
        # definition du handler de log de debogage
        DEBUG_LOGGER = logging.getLogger("rsyncDebug")
        DEBUG_LOGGER.info("Programme lance")
        DEBUG_LOGGER.debug("Log de debug")
    else:
        MAIN_LOGGER = creeLog(logPath)

    return MAIN_LOGGER


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    # MAIN_LOGGER = initLog("C:\\Users\\vvinc_000\\Desktop", "")
    # MAIN_LOGGER = initLog("/home/nicolas/Documents/Git/rsyncFTP", "")
    return 1


if __name__ == "__main__":
    monMain()
