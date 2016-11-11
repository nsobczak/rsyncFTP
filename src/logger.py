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


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation
def initLog(logPath, logConf):
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)
    :param logPath: chemin ou enregistrer le logger
    :param logConf: chemin ou trouver le .conf
    :return: MAIN_LOGGER
    :rtype: log
    """
    logging.config.fileConfig("rsyncFTP.conf")
    # logging.basicConfig(filename=os.path.join(logPath, "pioupiou.log"))

    # definition du handler
    MAIN_LOGGER = logging.getLogger("rsyncLocal")
    log2 = logging.getLogger("rsyncFile")

    MAIN_LOGGER.info("Programme lance")
    log2.info("Programme lance test file")

    return MAIN_LOGGER


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Test unitaire
def monMain():
    MAIN_LOGGER = initLog("/media/nicolas/DE581D27581CFFC7/Users/Nicolas/Documents/Ecole/ISEN/Python",
                          "/media/nicolas/DE581D27581CFFC7/Users/Nicolas/Documents/Ecole/ISEN/Python")


if __name__ == "__main__":
    monMain()
