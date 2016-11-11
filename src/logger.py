############
# rsyncFTP #
############

# TODO : Faire en sorte de pouvoir indiquer le chemin d'enregistrement du fichier log genere
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

    :param logPath:
    :return: MAIN_LOGGER
    :rtype: log
    """
    if os.path.isdir(logPath):
        nameFile = os.path.join(logPath, "rsyncFTP.log")
    elif os.path.isfile(logPath):
        nameFile = logPath
    else :
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
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    :param logPath: chemin ou enregistrer le logger
    :param logConf: chemin ou trouver le .conf
    :return: MAIN_LOGGER
    :rtype: log
    """
    if logPath == "":

        logging.config.fileConfig(logConf)
        # logging.basicConfig(filename=os.path.join(logPath, "pioupiou.log"))

        # definition du handler
        MAIN_LOGGER = logging.getLogger("rsyncLocal")
        log2 = logging.getLogger("rsyncFile")

        MAIN_LOGGER.info("Programme lance")
        log2.info("Programme lance test file")
    else :
        MAIN_LOGGER = creeLog(logPath)

    return MAIN_LOGGER


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    MAIN_LOGGER = initLog("C:\\Users\\vvinc_000\\Desktop","")


if __name__ == "__main__":
    monMain()
