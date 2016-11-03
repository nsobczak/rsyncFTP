############
# rsyncFTP #
############

# TODO : /
# ____________________________________________________________________________________________________
# Config

# Import
import logging


# ____________________________________________________________________________________________________
# ____________________________________________________________________________________________________
# Fonctions d'initialisation
def initLog():
    """
    log format
    logging.basicConfig(datefmt='', format='%asctime', level=logging.INFO)    :param fileName: nom du fichier dans lequel remplacer les liens
    :return: MAIN_LOGGER
    :rtype: log
    """
    logging.config.fileConfig("rsyncFTP.conf")
    # definition du handler
    MAIN_LOGGER = logging.getLogger("test_log")

    MAIN_LOGGER.info("Programme lance")
    # MAIN_LOGGER.critical("Ceci est une erreur critique !")
    # MAIN_LOGGER.warning("Ceci est un message de debogage !")
    return MAIN_LOGGER

# ____________________________________________________________________________________________________
